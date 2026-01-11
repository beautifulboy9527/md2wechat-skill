package main

import (
	"fmt"
	"os"

	"github.com/geekjourneyx/md2wechat-skill/internal/draft"
	"github.com/spf13/cobra"
	"go.uber.org/zap"
)

var testHTMLCmd = &cobra.Command{
	Use:   "test-draft <html_file> <cover_image>",
	Short: "Test creating WeChat draft from HTML file",
	Args:  cobra.ExactArgs(2),
	PreRunE: func(cmd *cobra.Command, args []string) error {
		return initConfig()
	},
	Run: func(cmd *cobra.Command, args []string) {
		htmlFile := args[0]
		coverImage := args[1]

		// 读取 HTML
		html, err := os.ReadFile(htmlFile)
		if err != nil {
			responseError(fmt.Errorf("read HTML file: %w", err))
			return
		}

		log.Info("testing draft creation",
			zap.Int("html_length", len(html)),
			zap.String("cover", coverImage))

		// 上传封面图片
		log.Info("uploading cover image", zap.String("path", coverImage))
		coverMediaID, err := uploadCoverImage(coverImage)
		if err != nil {
			responseError(fmt.Errorf("upload cover: %w", err))
			return
		}
		log.Info("cover uploaded", zap.String("media_id", maskMediaID(coverMediaID)))

		// 创建草稿
		svc := draft.NewService(cfg, log)
		result, err := svc.CreateDraft([]draft.Article{
			{
				Title:        "AI生成测试文章",
				Content:      string(html),
				Digest:       "这是AI生成的微信公众号文章测试",
				ThumbMediaID: coverMediaID,
				ShowCoverPic: 1,
			},
		})

		if err != nil {
			responseError(fmt.Errorf("create draft: %w", err))
			return
		}

		responseSuccess(map[string]any{
			"success":   true,
			"media_id":  result.MediaID,
			"draft_url": result.DraftURL,
			"message":   "Draft created successfully! You can check it in WeChat backend.",
		})
	},
}
