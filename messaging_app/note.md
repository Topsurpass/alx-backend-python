# General flow of the CI/CD pipeline and DevOps process

### Summary of each step and its role in modern DevOps, CI/CD, and containerized deployments

## Development (App Building):

This is the preliminary stage of the whole software development process. At this stage, developers - both Frontend and Backend, develop their applications respectively. This is where containerization of the application starts. During the development stage, developers may use different versions of packages and libraries, which, when merging code together, might result in conflicts and dependency issues. Dockerizing your application helps solve this issue. Developers save their dependencies in a file, e.g., in Python, `requirements.txt`, and in JavaScript, `package.json`. Once they have this in place, they can create a configuration to build a Docker image in a file called `Dockerfile` and specify the packages to install with their versions inside that image. Once the code is pushed, other developers working on it can create an image and run a container based on the Dockerfile. This ensures that they have the same environment and the same dependencies. With Docker, you do not need to install all of these dependencies on your local machine as you can just install them on your image or container, and that's all.

### Example: Dockerizing a Python Application

1. **Create a `requirements.txt` file**:
   `plaintext
 flask==2.0.1
 requests==2.25.1
 `
   Above file content can be achieve in python application by using this:
   `bash
 pip freeze > requirements.txt
 `

2. **Create a `Dockerfile`**:

   ```dockerfile
   # Use an official Python runtime as a parent image
   FROM python:3.8-slim

   # Set the working directory in the container
   WORKDIR /app

   # Copy the current directory contents into the container at /app
   COPY . /app

   # Install any needed packages specified in requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt

   # Make port 80 available to the world outside this container
   EXPOSE 80

   # Define environment variable
   ENV NAME World

   # Run app.py when the container launches
   CMD ["python3", "app.py"]
   ```

3. **Build the Docker image**:

   ```bash
   docker build -t my-python-app .
   ```

4. **Run the Docker container**:
   ```bash
   docker run -p 4000:80 my-python-app
   ```

### N.B:

    In some cases, you might need to access the shell inthe command, to do so, use the command below to access as the root user:

    ```bash
    docker exec -it --user root jenkins-container bash
    ```

### Example: Dockerizing a Node.js Application

1. **Create a `package.json` file**:

   ```json
   {
     "name": "my-node-app",
     "version": "1.0.0",
     "description": "A simple Node.js application",
     "main": "app.js",
     "scripts": {
       "start": "node app.js"
     },
     "dependencies": {
       "express": "^4.17.1"
     }
   }
   ```

2. **Create a `Dockerfile`**:

   ```dockerfile
   # Use an official Node runtime as a parent image
   FROM node:14

   # Set the working directory in the container
   WORKDIR /usr/src/app

   # Copy package.json and package-lock.json
   COPY package*.json ./

   # Install app dependencies
   RUN npm install

   # Bundle app source
   COPY . .

   # Make port 8080 available to the world outside this container
   EXPOSE 8080

   # Define environment variable
   ENV NODE_ENV=production

   # Run app.js when the container launches
   CMD ["node", "app.js"]
   ```

3. **Build the Docker image**:

   ```bash
   docker build -t my-node-app .
   ```

4. **Run the Docker container**:
   ```bash
   docker run -p 8080:8080 my-node-app
   ```

By following these steps, developers can ensure that their applications run consistently across different environments, avoiding the "it works on my machine" problem. Docker provides a standardized unit of software that packages up code and all its dependencies, making it easier to develop, ship, and run applications.

## CI/CD (Continuous Integration/Continuous Deployment)

### What is CI/CD?

CI/CD stands for Continuous Integration and Continuous Deployment/Delivery. It is a method to frequently deliver apps to customers by introducing automation into the stages of app development. The main concepts attributed to CI/CD are continuous integration, continuous deployment, and continuous delivery.

### Continuous Integration (CI)

CI is a development practice where developers integrate code into a shared repository frequently, preferably several times a day. Each integration can then be verified by an automated build and automated tests. CI aims to detect and fix integration issues earlier, improve software quality, and reduce the time it takes to validate and release new software updates.

### Continuous Deployment (CD)

CD is a software release process that uses automated testing to validate whether changes to a codebase are correct and stable for immediate autonomous deployment to a production environment. CD ensures that software can be reliably released at any time.

## Uses of CI/CD

- **Automated Testing**: Ensures that code changes do not break the existing functionality.
- **Automated Deployment**: Reduces the manual effort required to deploy applications.
- **Faster Release Cycles**: Enables more frequent releases of software.
- **Improved Collaboration**: Encourages collaboration among team members by integrating changes frequently.

## Advantages of CI/CD

- **Early Bug Detection**: Bugs are detected early in the development cycle.
- **Reduced Integration Issues**: Frequent integration reduces the risk of integration issues.
- **Faster Time to Market**: Automated processes speed up the release cycle.
- **Consistent Delivery**: Ensures consistent and reliable delivery of software.
- **Improved Quality**: Automated testing and deployment improve the overall quality of the software.

## Setting Up CI/CD

### Example with Jenkins

#### What is Jenkins?

Jenkins is an open-source automation server designed to help developers and teams automate tasks related to building, testing, and deploying software. It's a key tool in the DevOps ecosystem because it simplifies continuous integration (CI) and continuous delivery (CD), ensuring that code changes are automatically tested and deployed quickly and reliably.

Think of Jenkins as your software-building assistant — it automates repetitive tasks so developers can focus on writing code instead of worrying about deployment, testing, or builds.

#### Why Use Jenkins?

- Automation: Automates tasks like building your code, running tests, and deploying to servers.
- Continuous Integration (CI): Allows developers to merge their code changes into a shared repository multiple times a day, with automated testing to catch issues early.
- Continuous Delivery (CD): Streamlines the process of delivering new code to production, reducing downtime.
- Plugins: Offers over 1,800 plugins to integrate with tools like GitHub, Docker, Kubernetes, Slack, and more.
- Customizable Pipelines: Lets you create pipelines (sequences of steps) to define how your code is built, tested, and deployed.
- Containerized Workflows: Build Docker images for your application and push them to container registries like Docker Hub.

1. **Install Jenkins**: Run jenkins in a docker container by executing the following command

   ```bash
   docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
   ```

   **This command will**:

   - Pull the latest Long-Term Support (LTS) Jenkins image.
   - Expose Jenkins on port 8080.
   - Map the Jenkins home directory to the host machine to persist data.

2. **Configure Jenkins**:

   - Get your admin password by running this command:

   ```bash
      # Open interactive shell of the jenkins container
       docker -exec -it --user root <name of your jenkins container>
   ```

   ```bash
      # Run this to get the admin password
       cat /var/lib/jenkins/secrets/initialAdminPassword
   ```

   - Access Jenkins at `http://localhost:8080`
   - Input your admin password when propted
   - Follow the setup wizard to install recommended plugins and create an admin user.
   - Create your first pipeline or job.

3. **Setting up a Jenkins Pipeline**:

   - Create a New Pipeline Job:
   - Go to the Jenkins dashboard, click "New Item", and select "Pipeline".
   - Write a Jenkinsfile: A Jenkinsfile defines your CI/CD pipeline. Example below

   ```groovy
       pipeline {
           agent any
           stages {
               stage('Build') {
                   steps {
                       echo 'Building the application...'
                   }
               }
               stage('Test') {
                   steps {
                       echo 'Running tests...'
                   }
               }
               stage('Deploy') {
                   steps {
                       echo 'Deploying the application...'
                   }
               }
           }
       }
   ```

4. **Run the Pipeline**:
   - Save the job and click "Build Now" to see your pipeline execute step by step.

### N.B:

1. In many cases, your pipeline might not success fully build as the container where your jenkins is running might not have some pacakge or library installed on it. In this case, open the container shell and install them.
2. Alternatively, ensure that these packages are included in your requirements.py file and create a stage to do the installation.
3. If you are using jenkins as user on the bash, kindly give necessary permission to jenkins user or switch to root and install.
4. Note that if you delete the container where jenkins is running, all of the installation and setup will bve deleted and you will have to start afresh again by creating new container from the image.

### Real-World Examples of Jenkins Usage

1. Building a Web App:
   Automatically build and deploy a React or Angular application when developers push code to GitHub.
2. Containerized Deployment:
   Build a Docker image for your Node.js app, push it to Docker Hub, and deploy it to Kubernetes.
3. Mobile App Development:
   Compile Android or iOS apps, run tests on a cloud-based emulator, and deploy the app to Google Play or the App Store.
4. Integration with Git:
   Set up Jenkins to pull the latest code changes from GitHub, run tests, and notify developers on Slack if something fails.
5. In cases where your pipeline needs to run docker commands within it's container, you will have to install docker inside the container to achieve this. Cases where you might need it includes when you need to build and push an image of your app after being tested to registry like docker hub. In this instance, you will have to:

- Make sure the Jenkins server has Docker installed and running.
- Grant Jenkins user permission to run Docker commands (add the user to the docker group):

```bash
// switch to root user and run this command
sudo usermod -aG docker jenkins
```

### Example with GitHub Actions

1. **Create a GitHub Actions Workflow**:

   - Create a `.github/workflows/main.yml` file in your repository root directory.

   ```yaml
   name: CI/CD Pipeline

   on:
     push:
       branches:
         - main

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout code
           uses: actions/checkout@v2

         - name: Set up Node.js
           uses: actions/setup-node@v2
           with:
             node-version: "14"

         - name: Install dependencies
           run: npm install

         - name: Run tests
           run: npm test

         - name: Build project
           run: npm run build

         - name: Deploy
           run: npm run deploy
   ```

2. Push your code to github and check under the action tab for the execution of the jobs in your workflow.

## Jenkins vs. GitHub Actions

### Jenkins

- **Pros**:

  - Highly customizable with a wide range of plugins.
  - Can be hosted on-premises, providing more control over the environment.
  - Supports complex workflows and pipelines.

- **Cons**:
  - Requires maintenance and management of the Jenkins server.
  - Steeper learning curve for beginners.

### GitHub Actions

- **Pros**:

  - Integrated with GitHub, making it easy to set up and use.
  - No need to manage servers or infrastructure.
  - Supports a wide range of actions and workflows.

- **Cons**:
  - Limited to GitHub repositories.
  - Less customizable compared to Jenkins.

## Differences Between CI and CD

- **Continuous Integration (CI)**:

  - Focuses on integrating code changes frequently.
  - Automated builds and tests are run to ensure code quality.
  - Aims to detect and fix integration issues early.

- **Continuous Deployment (CD)**:
  - Focuses on deploying code changes automatically to production.
  - Ensures that the code is always in a deployable state.
  - Reduces the manual effort required for deployment.

---

## Triggering Jenkins Pipelines on GitHub Push and Pull Events

This guide will help you configure Jenkins to automatically trigger a pipeline when code is pushed to or a pull request is created/updated in a GitHub repository.

---

### Prerequisites

1. **Jenkins Setup:**

   - Ensure Jenkins is installed and running.
   - Install the following Jenkins plugins:
     - **GitHub Integration Plugin**
     - **Pipeline Plugin** or **Multibranch Pipeline Plugin**
   - Jenkins should be accessible over the internet or the network (e.g., via `http://<your-jenkins-url>`).

2. **GitHub Repository:**

   - You must have admin access to the repository.
   - Ensure the repository contains a `Jenkinsfile` for the pipeline configuration.

3. **Webhooks:**
   - Jenkins must have a public-facing URL for GitHub to send webhook events (e.g., using tools like [ngrok](https://ngrok.com) for local testing).

---

## Step-by-Step Configuration

### 1. Configure the Jenkins Job

#### **For a Single Branch Pipeline Job:**

1. Log in to Jenkins and create a new job:
   - Select **Pipeline** or **Freestyle Project** as the job type.
2. Under **Source Code Management**, select **Git** and provide:
   - Repository URL: `<GitHub Repository HTTPS/SSH URL>`
   - Branch: `main`, `master`, or the branch to be built.
3. Scroll down to **Build Triggers** and check:
   - **GitHub hook trigger for GITScm polling**
4. Save the job configuration.

#### **For a Multibranch Pipeline Job:**

1. Create a new job:
   - Select **Multibranch Pipeline** as the job type.
2. Under **Branch Sources**, click **Add Source** and select **GitHub**.
   - Provide your repository details.
   - Authenticate using a GitHub token if required.
3. Under the **Scan Multibranch Pipeline Triggers** section:
   - Set a periodic scan schedule (optional).
4. Save the job configuration.

---

### 2. Configure GitHub Webhooks

1. Go to your GitHub repository and navigate to:
   **Settings** > **Webhooks** > **Add Webhook**.
2. Fill in the webhook details:
   - **Payload URL**: `http://<your-jenkins-url>/github-webhook/`
   - **Content type**: `application/json`
   - **Events to trigger:**
     - Select **Just the push event** and **Pull request** or choose **Send me everything**.
3. Click **Add Webhook** to save.

---

### 3. Verify Webhook and Pipeline Integration

1. Push a change to the repository or create a pull request.
2. Go to Jenkins and check the job's **Build History** to confirm that the pipeline was triggered.

---

## Difference Between Single Branch Pipeline and Multibranch Pipeline

| Feature                   | Single Branch Pipeline                                           | Multibranch Pipeline                                                              |
| ------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Job Type**              | Works with one specific branch (e.g., `main` or `dev`).          | Automatically detects and builds all branches in the repository.                  |
| **Setup Complexity**      | Simple to set up; requires minimal configuration.                | More complex setup due to scanning all branches.                                  |
| **Branch Management**     | Requires creating a separate job for each branch.                | Automatically scans and manages all branches.                                     |
| **Use Case**              | Ideal for projects with a single main branch or static branches. | Best for repositories with multiple feature branches or dynamic branch workflows. |
| **Build Trigger**         | Triggered by specific branch events (e.g., `main` branch push).  | Triggers based on changes in any branch.                                          |
| **Efficiency**            | Limited to one branch, no unnecessary scans.                     | Can be resource-intensive due to branch scanning.                                 |
| **Jenkins Configuration** | Configured manually for a single branch.                         | Automatically configures pipeline jobs for all branches with a `Jenkinsfile`.     |

---

## Optional: Advanced Pipeline Logic

To customize your pipeline based on the trigger type (push or pull request), use the `CHANGE_ID` or `BRANCH_NAME` environment variables in your `Jenkinsfile`.

### Example `Jenkinsfile`:

```groovy
pipeline {
    agent any
    environment {
        EVENT_TYPE = env.CHANGE_ID ? 'Pull Request' : 'Push'
    }
    stages {
        stage('Trigger Info') {
            steps {
                echo "Triggered by: ${EVENT_TYPE}"
                echo "Branch: ${env.BRANCH_NAME}"
            }
        }
        stage('Build') {
            steps {
                echo "Building the project..."
                // Add your build commands here
            }
        }
    }
}
```

## Kubernetes: Orchestrating Containerized Applications

Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform designed to automate the deployment, scaling, and management of containerized applications. Originally developed by Google and now maintained by the Cloud Native Computing Foundation (CNCF), Kubernetes has become the de facto standard for managing modern cloud-native workloads.

### Brief introduction on Kubenetes and minikube relationship

Minikube is a tool that sets up a local Kubernetes cluster on a single machine, usually for development or testing purposes. A kubenetes cluster is a set of machines that run containerized applications. But how to explain that simply? Maybe compare it to a team where each member has a role. The cluster is like the whole team working together. Nodes. In Kubernetes, nodes are the individual machines, either physical or virtual. There are master nodes (control plane) and worker nodes. The control plane manages the cluster, and worker nodes run the applications. But Minikube uses one machine that acts as both master and worker.

### Understanding Kubernetes Architecture

**Clusters**: The Foundation of Kubernetes
A Kubernetes cluster is a collection of machines (physical or virtual) that work collectively to run containerized applications. Think of a cluster as a highly coordinated team: each member (machine) has a specialized role, and together, they ensure applications run reliably, scale seamlessly, and recover from failures automatically.

**Nodes**: The Workers of the Cluster
Nodes are the individual machines within a Kubernetes cluster. They are categorized into two types:

1. **Control Plane (Master Nodes)**:
   The control plane is the brain of the cluster, responsible for global decision-making and managing the cluster’s desired state. Key components include:

   - API Server: The front-end for cluster interactions.
   - etcd: A distributed key-value store for cluster data.
   - Scheduler: Assigns workloads to worker nodes.
   - Controller Manager: Monitors and repairs cluster state (e.g., restarting failed containers).
   - Cloud Controller Manager: Integrates with cloud provider APIs (optional).

2. **Worker Nodes**:
   These execute application workloads. Each worker node hosts:

   - Kubelet: An agent communicating with the control plane.
   - kube-proxy: Manages network rules for communication.
   - Container Runtime: Software like Docker or containerd to run containers.

### Minikube: Local Kubernetes Development Made Simple

**What is Minikube?**
Minikube is a lightweight, open-source tool that provisions a single-node Kubernetes cluster on a local machine (e.g., a developer’s laptop). It simulates a production-grade cluster in a simplified environment, making it ideal for:

- Local development and testing.
- Learning Kubernetes concepts.
- Experimenting with configurations before deploying to production.
  Unlike multi-node production clusters, Minikube combines the control plane and worker node roles into a single machine, reducing resource overhead while retaining core Kubernetes functionality.
  Kubernetes is like the manager of a complex restaurant chain, ensuring your apps (cooks) are always running, balanced, and serving users efficiently. It’s designed for modern cloud-based applications and helps businesses save time, effort, and money while maintaining high reliability and scalability.

#### Key Features of Minikube

1.  Single-Node Cluster: Simulates master and worker roles on one machine.
2.  Cross-Platform Support: Runs on Windows, macOS, and Linux.
3.  Addon Ecosystem: Extends functionality with DNS, dashboard, and ingress controllers.
4.  Isolated Environment: Sandboxes development workflows without impacting production.

#### N.B:

1.  When we create a Kubernetes cluster, there is one control plane (master node) that manages the entire cluster, no matter how many worker nodes exist. The control plane is responsible for decision-making (like scheduling workloads, monitoring nodes, and managing cluster states).
2.  All other nodes in the cluster are worker nodes, and they are responsible for running your applications. The control plane tells these worker nodes what to do, but the worker nodes themselves don’t make management decisions—they just execute.
3.  Inside each worker node, you have pods, and the pods are where your containerized applications live. A pod is the smallest deployable unit in Kubernetes and can contain one or more tightly coupled containers.
4.  Pods can communicate with each other—even if they’re on different worker nodes—using Kubernetes networking. And we use services to expose pods, making them accessible to other pods or external users.

### What can cause a node to go down?

A node going down means that the machine (virtual or physical) running that node is no longer operational or reachable. Here are some common reasons why this might happen:

1.  Hardware failure: If a physical server hosting the node crashes (e.g., due to a power outage or disk failure), the node goes down.
2.  Network issues: If there’s a network connectivity problem, the node might become unreachable by the control plane.
3.  Resource exhaustion: If the node runs out of resources (like CPU, memory, or disk space), it might crash or become non-functional.
4.  Configuration issues: Misconfigured Kubernetes components or software (e.g., kubelet, container runtime) can cause the node to fail.
5.  Operating system crash: If the operating system hosting the node crashes (e.g., due to kernel panic), the node will go down.
6.  Manual intervention: Someone might accidentally or intentionally shut down the node.
7.  Software updates/reboots: During maintenance, if the node is rebooted or software updates are applied, it will temporarily go down.

### Installation of kubenetes with minikube

**Order of Installation**

- Install Docker (or an alternative container runtime).
- Install Minikube (it can install before or after Docker, but Docker is necessary for Minikube's default configuration).
- Install kubectl to interact with the Kubernetes cluster created by Minikube.

```bash
# Kubenetes installation For Linux (Debian/Ubuntu)
sudo apt-get update && sudo apt-get install -y kubectl
```

```bash
# Minikube installation
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

```bash
# Start Minikube
minikube start --driver=<driver-name>  # e.g., virtualbox, hyperkit
```

```bash
# Verify cluster status
kubectl get nodes
```

```bash
# Deploy sample application
kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4
kubectl expose deployment hello-minikube --type=NodePort --port=8080
```

```bash
# Access the app
minikube service hello-minikube
```
