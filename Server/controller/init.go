package controller

import (
	"agentencryption/core"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func InitServer() *gin.Engine {
	route := gin.Default()
	route.Use(cors.Default())
	route.POST("/Register", core.Register)
	route.POST("/GetModel", core.GetModel)
	return route
}
