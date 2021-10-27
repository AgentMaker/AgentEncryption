package main

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func InitServer() *gin.Engine {
	route := gin.Default()
	route.Use(cors.Default())
	route.POST("/Register")
	return route
}
