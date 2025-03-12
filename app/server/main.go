package main

import (
	"fmt"
	"go-postgres/router"
	"log"
	"net/http"

	"github.com/rs/cors"
)

func main() {
	r := router.Router()
	// fs := http.FileServer(http.Dir("build"))
	// http.Handle("/", fs)

	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://192.168.40.211:8082", "http://localhost:8082"},
		AllowCredentials: true,
	})

	handler := c.Handler(r)

	fmt.Println("Starting server on the port 8084...")

	log.Fatal(http.ListenAndServe(":8084", handler))
}
