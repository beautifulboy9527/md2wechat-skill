package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/geekjourneyx/md2wechat-skill/internal/config"
	"github.com/geekjourneyx/md2wechat-skill/internal/draft"
	"github.com/geekjourneyx/md2wechat-skill/internal/image"
	"github.com/spf13/cobra"
	"go.uber.org/zap"
)

var (
	cfg *config.Config
	log *zap.Logger
)

// initConfig 初始化配置（延迟加载，允许 help 命令无需配置）
func initConfig() error {
	if cfg != nil && log != nil {
		return nil
	}

	var err error
	cfg, err = config.Load()
	if err != nil {
		return err
	}

	log, err = zap.NewProduction()
	if err != nil {
		return err
	}

	return nil
}

func main() {
	var rootCmd = &cobra.Command{
		Use:   "md2wechat",
		Short: "Markdown to WeChat Official Account converter",
		Long: `md2wechat converts Markdown articles to WeChat Official Account format
and supports uploading materials and creating drafts.

Environment Variables:
  WECHAT_APPID                   WeChat Official Account AppID (required)
  WECHAT_SECRET                  WeChat API Secret (required)
  IMAGE_API_KEY                  Image generation API key (for AI images)
  IMAGE_API_BASE                 Image API base URL (default: https://api.openai.com/v1)
  COMPRESS_IMAGES                Compress images > 1920px (default: true)
  MAX_IMAGE_WIDTH                Max image width in pixels (default: 1920)

Examples:
  md2wechat upload_image ./photo.jpg
  md2wechat download_and_upload https://example.com/image.jpg
  md2wechat generate_image "A cute cat"
  md2wechat create_draft draft.json`,
		SilenceErrors: true,
		SilenceUsage:  true,
	}

	// upload_image command
	var uploadImageCmd = &cobra.Command{
		Use:   "upload_image <file_path>",
		Short: "Upload local image to WeChat material library",
		Args:  cobra.ExactArgs(1),
		PreRunE: func(cmd *cobra.Command, args []string) error {
			return initConfig()
		},
		Run: func(cmd *cobra.Command, args []string) {
			filePath := args[0]
			processor := image.NewProcessor(cfg, log)
			result, err := processor.UploadLocalImage(filePath)
			if err != nil {
				responseError(err)
				return
			}
			responseSuccess(result)
		},
	}
	rootCmd.AddCommand(uploadImageCmd)

	// download_and_upload command
	var downloadAndUploadCmd = &cobra.Command{
		Use:   "download_and_upload <url>",
		Short: "Download online image and upload to WeChat",
		Args:  cobra.ExactArgs(1),
		PreRunE: func(cmd *cobra.Command, args []string) error {
			return initConfig()
		},
		Run: func(cmd *cobra.Command, args []string) {
			url := args[0]
			processor := image.NewProcessor(cfg, log)
			result, err := processor.DownloadAndUpload(url)
			if err != nil {
				responseError(err)
				return
			}
			responseSuccess(result)
		},
	}
	rootCmd.AddCommand(downloadAndUploadCmd)

	// generate_image command
	var generateImageCmd = &cobra.Command{
		Use:   "generate_image <prompt>",
		Short: "Generate image via AI and upload to WeChat",
		Args:  cobra.ExactArgs(1),
		PreRunE: func(cmd *cobra.Command, args []string) error {
			return initConfig()
		},
		Run: func(cmd *cobra.Command, args []string) {
			prompt := args[0]
			processor := image.NewProcessor(cfg, log)
			result, err := processor.GenerateAndUpload(prompt)
			if err != nil {
				responseError(err)
				return
			}
			responseSuccess(result)
		},
	}
	rootCmd.AddCommand(generateImageCmd)

	// create_draft command
	var createDraftCmd = &cobra.Command{
		Use:   "create_draft <json_file>",
		Short: "Create WeChat draft article from JSON file",
		Args:  cobra.ExactArgs(1),
		PreRunE: func(cmd *cobra.Command, args []string) error {
			return initConfig()
		},
		Run: func(cmd *cobra.Command, args []string) {
			jsonFile := args[0]
			svc := draft.NewService(cfg, log)
			result, err := svc.CreateDraftFromFile(jsonFile)
			if err != nil {
				responseError(err)
				return
			}
			responseSuccess(result)
		},
	}
	rootCmd.AddCommand(createDraftCmd)

	// convert command
	rootCmd.AddCommand(convertCmd)

	// config command
	rootCmd.AddCommand(configCmd)

	// test-draft command
	rootCmd.AddCommand(testHTMLCmd)

	// Execute
	if err := rootCmd.Execute(); err != nil {
		responseError(err)
		os.Exit(1)
	}
}

func responseSuccess(data any) {
	response := map[string]any{
		"success": true,
		"data":    data,
	}
	printJSON(response)
}

func responseError(err error) {
	response := map[string]any{
		"success": false,
		"error":   err.Error(),
	}
	printJSON(response)
	os.Exit(1)
}

func printJSON(v any) {
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	encoder.SetEscapeHTML(false)
	if err := encoder.Encode(v); err != nil {
		fmt.Fprintf(os.Stderr, "JSON encode error: %v\n", err)
		os.Exit(1)
	}
}

// maskMediaID 遮蔽 media_id 用于日志
func maskMediaID(id string) string {
	if len(id) < 8 {
		return "***"
	}
	return id[:4] + "***" + id[len(id)-4:]
}
