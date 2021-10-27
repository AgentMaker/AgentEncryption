package main

import (
	"agentencryption/controller"
	"log"
)

func main() {
	router := controller.InitServer()
	err := router.Run("2333")
	if err != nil {
		log.Fatalln("Failed to start server: ", err)
	}
}
