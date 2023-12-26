package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"os"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq" // Specifically for PostgreSQL
)

type Attraction struct {
	name    string // `json:"name"`
	city    string // `json:"city"`
	address string // `json:"address"`
}

var (
	DBNAME     string
	DBUSER     string
	DBPASSWORD string
	DBHOST     string
	DBPORT     string
	connStr    string
)

func main() {
	if err := godotenv.Load("../../../.env"); err != nil {
		log.Fatal("Could not load environment variables with godotenv.")
	}

	DBNAME = os.Getenv("DBNAME")
	DBUSER = os.Getenv("DBUSER")
	DBPASSWORD = os.Getenv("DBPASSWORD")
	DBHOST = os.Getenv("DBHOST")
	DBPORT = os.Getenv("DBPORT")

	// connStr = fmt.Sprintf("dbname=%s user=%s password=%s host=%s port=%s sslmode=disable", DBNAME, DBUSER, DBPASSWORD, DBHOST, DBPORT)

	// router := gin.Default()
	// router.GET("/attraction", getRandomAttraction)
	// router.Run("localhost:8080")
	lambda.Start(handler)
}

func handler(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	log.Println("In handler...")
	attraction := retrieveRandomAttraction()
	attraction_string := fmt.Sprintf("Name: %s, City: %s, Address: %s", attraction.name, attraction.city, attraction.address)
	response := events.APIGatewayProxyResponse{
		StatusCode: 200,
		Body:       attraction_string,
	}

	return response, nil
}

func retrieveRandomAttraction() Attraction {
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
			name:    name,
			city:    city,
			address: address,
		}
	}
	return attraction
}

// func getRandomAttraction(c *gin.Context) {
// 	attraction := retrieveRandomAttraction()
// 	fmt.Printf("Old Attraction Info: Name: %s | City: %s | Address: %s \n", attraction.name, attraction.city, attraction.address)

// 	// Check if city matches address
// 	// e.g)
// 	// {
// 	// 	"address": "333 Gladwin Rd, Abbotsford, BC V2S 8A7, Canada",
// 	// 	"city": "Langley",
// 	// 	"name": "Applebarn Pumpkin Farm (Taves Farms)"
// 	// }
// 	// address := attraction.address
// 	// address_components := strings.Split(address, ", ")
// 	// city := address_components[1]
// 	// if city != address {
// 	// 	_, updateErr := db.Exec("UPDATE bsee SET city = %s WHERE address = %s", city, address) //Exec is for read-only database migrations
// 	// 	if updateErr != nil {
// 	// 		log.Fatal("Update error")
// 	// 		log.Fatal(updateErr)
// 	// 	}
// 	// 	c.JSON(http.StatusOK, gin.H{
// 	// 		"name":    attraction.name,
// 	// 		"city":    attraction.city,
// 	// 		"address": attraction.address,
// 	// 	})
// 	// 	fmt.Printf("Updated. Responded with attraction: Name: %s | City: %s | Address: %s \n", attraction.name, city, attraction.address)
// 	// }
// 	c.JSON(http.StatusOK, gin.H{
// 		"name":    attraction.name,
// 		"city":    attraction.city,
// 		"address": attraction.address,
// 	})
// 	fmt.Printf("Responded with attraction: Name: %s | City: %s | Address: %s \n", attraction.name, attraction.city, attraction.address)

// }
