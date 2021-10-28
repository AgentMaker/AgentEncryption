package main

import (
	"agentencryption/controller"
	"log"
)

func main() {
	router := controller.InitServer()
	err := router.Run(":6666")
	if err != nil {
		log.Fatalln("Failed to start server: ", err)
	}
}
