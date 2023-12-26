async function getAttraction() {
    const response = await fetch("http://localhost:8080/attraction")
    const attraction = await response.json()
    console.log(attraction)
    return attraction
}

getAttraction()
