package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"os"

	"github.com/aws/aws-lambda-go/lambda"
)

type MyEvent struct {
	Name string `json:"name"`
}

type Attraction struct {
	Name    string `json:"name"`
	City    string `json:"city"`
	Address string `json:"address"`
}

var (
	DBNAME     string
	DBUSER     string
	DBPASSWORD string
	DBHOST     string
	DBPORT     string
	connStr    string
)

func HandleRequest(ctx context.Context, event *Attraction) (*string, error) {
	// TODO
	if event == nil {
		return nil, fmt.Errorf("recieved nil event")
	}
	attraction := retrieveRandomAttraction()
	message := fmt.Sprintf("%s %s %s", attraction.Name, attraction.City, attraction.Address)
	return &message, nil

}

func main() {
	lambda.Start(HandleRequest)
}

func retrieveRandomAttraction() Attraction {
	DBNAME = os.Getenv("DBNAME")
	DBUSER = os.Getenv("DBUSER")
	DBPASSWORD = os.Getenv("DBPASSWORD")
	DBHOST = os.Getenv("DBHOST")
	DBPORT = os.Getenv("DBPORT")

	connStr = fmt.Sprintf("dbname=%s user=%s password=%s host=%s port=%s sslmode=disable", DBNAME, DBUSER, DBPASSWORD, DBHOST, DBPORT)
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}

	row_count := 1312
	id := rand.Intn(row_count)
	query := fmt.Sprintf("SELECT name, city, address from bsee WHERE id=%d", rand.Intn(id))
	rows, err := db.Query(query)

	if err != nil {
		log.Fatal(err)
	}

	defer rows.Close()

	var name string
	var city string
	var address string
	var attraction Attraction
	for rows.Next() {
		err := rows.Scan(&name, &city, &address)
		if err != nil {
			log.Fatal(err)
		}

		attraction = Attraction{
			Name:    name,
			City:    city,
			Address: address,
		}
	}
	return attraction
}
