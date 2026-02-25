FROM golang:1.25-alpine

WORKDIR /app

RUN apk add --no-cache git

COPY api/  .

RUN go mod tidy

RUN go build -o main .

EXPOSE 8080

CMD ["./main"]
