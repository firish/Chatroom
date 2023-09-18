# Use the official Node.js image as a base image
FROM node:16.16.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json files to the container
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy all files from the current directory to the container
COPY . .

# Expose port 3000 for the React development server
EXPOSE 3000

# Command to run the React development server
CMD ["npm", "start"]
