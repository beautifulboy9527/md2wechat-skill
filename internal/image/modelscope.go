package image

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/geekjourneyx/md2wechat-skill/internal/config"
)

type ModelScopeProvider struct {
	apiKey  string
	baseURL string
	model   string
}

func NewModelScopeProvider(cfg *config.Config) (*ModelScopeProvider, error) {
	model := cfg.ImageModel
	if model == "" {
		model = "Tongyi-MAI/Z-Image-Turbo"
	}
	return &ModelScopeProvider{
		apiKey:  cfg.ImageAPIKey,
		baseURL: cfg.ImageAPIBase,
		model:   model,
	}, nil
}

func (p *ModelScopeProvider) Name() string {
	return "modelscope"
}

type modelScopeGenerationRequest struct {
	Model  string `json:"model"`
	Prompt string `json:"prompt"`
}

type modelScopeGenerationResponse struct {
	TaskID  string `json:"task_id"`
	Message string `json:"message"`
	Code    string `json:"code"`
}

type modelScopeTaskResponse struct {
	TaskID       string   `json:"task_id"`
	TaskStatus   string   `json:"task_status"` // PENDING, RUNNING, SUCCEED, FAILED
	OutputImages []string `json:"output_images,omitempty"`
	Message      string   `json:"message,omitempty"`
}

func (p *ModelScopeProvider) Generate(ctx context.Context, prompt string) (*GenerateResult, error) {
	// 1. Submit task
	reqBody := modelScopeGenerationRequest{
		Model:  p.model,
		Prompt: prompt,
	}
	jsonBody, err := json.Marshal(reqBody)
	if err != nil {
		return nil, fmt.Errorf("marshal request: %w", err)
	}

	// Ensure baseURL ends with /
	baseURL := p.baseURL
	if baseURL[len(baseURL)-1] != '/' {
		baseURL += "/"
	}

	req, err := http.NewRequestWithContext(ctx, "POST", baseURL+"v1/images/generations", bytes.NewBuffer(jsonBody))
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+p.apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-ModelScope-Async-Mode", "true")

	client := &http.Client{
		Timeout: 30 * time.Second,
	}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("do request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("api error status=%d body=%s", resp.StatusCode, string(body))
	}

	var genResp modelScopeGenerationResponse
	if err := json.NewDecoder(resp.Body).Decode(&genResp); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}

	taskID := genResp.TaskID
	if taskID == "" {
		return nil, fmt.Errorf("no task_id returned")
	}

	// 2. Poll for result
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	// Max wait time 60 seconds
	timeoutCtx, cancel := context.WithTimeout(ctx, 60*time.Second)
	defer cancel()

	for {
		select {
		case <-timeoutCtx.Done():
			return nil, fmt.Errorf("polling timeout")
		case <-ticker.C:
			taskURL := fmt.Sprintf("%sv1/tasks/%s", baseURL, taskID)
			reqTask, err := http.NewRequestWithContext(ctx, "GET", taskURL, nil)
			if err != nil {
				return nil, fmt.Errorf("create task request: %w", err)
			}
			reqTask.Header.Set("Authorization", "Bearer "+p.apiKey)
			reqTask.Header.Set("X-ModelScope-Task-Type", "image_generation")

			respTask, err := client.Do(reqTask)
			if err != nil {
				// Log error but maybe continue? Or fail?
				return nil, fmt.Errorf("check task status: %w", err)
			}
			defer respTask.Body.Close()

			if respTask.StatusCode != http.StatusOK {
				body, _ := io.ReadAll(respTask.Body)
				return nil, fmt.Errorf("task api error status=%d body=%s", respTask.StatusCode, string(body))
			}

			var taskData modelScopeTaskResponse
			if err := json.NewDecoder(respTask.Body).Decode(&taskData); err != nil {
				return nil, fmt.Errorf("decode task response: %w", err)
			}

			if taskData.TaskStatus == "SUCCEED" {
				if len(taskData.OutputImages) == 0 {
					return nil, fmt.Errorf("task succeeded but no images returned")
				}
				return &GenerateResult{
					URL:   taskData.OutputImages[0],
					Model: p.model,
				}, nil
			} else if taskData.TaskStatus == "FAILED" {
				return nil, fmt.Errorf("task failed: %s", taskData.Message)
			}
			// Continue polling if PENDING or RUNNING
		}
	}
}
