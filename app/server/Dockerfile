# Use a lightweight base image
FROM golang:1.24 as builder

# Set the working directory inside the container
WORKDIR /app/server

# Copy go.mod and go.sum for dependency resolution
COPY go.mod go.sum ./
RUN go mod tidy && go mod vendor

# Copy the rest of the app source
COPY . .

# Build the Go binary
RUN go build -o server .

# Use a smaller base image for the final container
FROM gcr.io/distroless/base-debian12

# Set the working directory
WORKDIR /root/

# Copy the compiled binary from the builder stage
COPY --from=builder /app/server .

# Expose the application port
EXPOSE 8082

# Run the server
CMD ["./server"]
