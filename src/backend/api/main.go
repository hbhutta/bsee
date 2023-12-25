package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"

	_ "github.com/lib/pq" // Specifically for PostgreSQL
)

const (
	DBName     = "postgres"
	DBHost     = "localhost"
	DBPort     = 5432
	DBUser     = "postgres"
	DBPassword = "R1a4786$"
)

type Attraction struct {
	name    string
	city    string
	address string
}

func main() {
	connStr := fmt.Sprintf("dbname=%s user=%s password=%s host=%s port=%d sslmode=disable", DBName, DBUser, DBPassword, DBHost, DBPort)
	fmt.Println(connStr)
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
	for rows.Next() {
		var name string
		var city string
		var address string
		err := rows.Scan(&name, &city, &address)
		if err != nil {
			log.Fatal(err)
		}

		attraction := Attraction{
			name:    name,
			city:    city,
			address: address,
		}
		fmt.Printf("(Name: %s | City: %s | Address: %s)\n", attraction.name, attraction.city, attraction.address)
	}
}
