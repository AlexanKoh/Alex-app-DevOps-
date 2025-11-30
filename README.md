# Flask MySQL Application

A simple web application built with Flask and MySQL database, supporting both Docker Compose deployment and full GitOps pipeline with Argo CD in Kubernetes.

![AlexanKoh's GitHub Stats](https://github-readme-stats.vercel.app/api?username=AlexanKoh&show_icons=true&theme=radical)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=AlexanKoh&layout=compact&theme=radical&hide=html,css)
![GitHub Actions](https://github.com/AlexanKoh/Alex-app-DevOps-/actions/workflows/docker-build.yml/badge.svg)
![Docker Build](https://img.shields.io/badge/Docker-Build%20Passing-success)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-blue)
![ArgoCD](https://img.shields.io/badge/ArgoCD-Synced-green)

## Architecture

- **Frontend**: Flask Python application
- **Database**: MySQL 8.0
- **Infrastructure**: Terraform + Ansible + Argo CD
- **Containerization**: Docker + Docker Compose

## Project Structure

```
.
├── Ansible/                 # Ansible playbooks for Kubernetes setup
├── ArgoCD/                  # Argo CD configuration for GitOps
├── Terraform/               # Infrastructure as Code (Azure AKS)
├── k8s-manifests/           # Kubernetes manifests for the application
├── app.py                   # Main Flask application
├── database.py              # Database module
├── docker-compose.yml       # Local deployment
├── Dockerfile               # Docker image build
├── requirements.txt         # Python dependencies
└── init.sql                 # Database initialization
```

### Local Deployment with Docker Compose

1. **Create .env file:**
```bash
cp .env.example .env
# Edit .env file with your settings
```

2. **Start the application:**
```bash
docker-compose up -d
```

3. **Verify it's working:**
```bash
curl http://localhost:5000/health
```

The application will be available at: `http://localhost:5000`

### Automated Docker Builds with GitHub Actions
The project includes GitHub Actions workflow that automatically builds and pushes Docker images to GitHub Container Registry:
`Build_and_Push_AlexApp.yml`

### Kubernetes Cluster Deployment with GitOps

#### 1. Create AKS Cluster in Azure

```bash
cd Terraform/
terraform init
terraform apply -auto-approve
terraform output -raw kube_config > ../kubeconfig.yaml
cd ..
```

#### 2. Verify Cluster Connection

```bash
kubectl --kubeconfig=kubeconfig.yaml get nodes
```

#### 3. Run Deployment Pipeline

```bash
# Basic cluster setup (namespace, secrets, metrics server)
ansible-playbook Ansible/setup-cluster.yml

# Install Argo CD
ansible-playbook ArgoCD/playbook.yml

# Register application in Argo CD
ansible-playbook ArgoCD/register-app.yml
```

#### 4. Verify Deployment

```bash
# Check application status
kubectl --kubeconfig=kubeconfig.yaml get all -n flask-app

# Get external IP for access
kubectl --kubeconfig=kubeconfig.yaml get svc web-service -n flask-app

# Check health endpoint
curl http://<EXTERNAL-IP>:5000/health
```

## 🔧 Configuration

### Environment Variables

- `DB_HOST` - database host
- `DB_PORT` - database port (default: 3306)
- `DB_USER` - database user
- `DB_PASSWORD` - database password
- `DB_NAME` - database name
- `DEBUG` - debug mode (True/False)

### Kubernetes Features

- **Horizontal Pod Autoscaler** - automatic scaling based on CPU and memory
- **Health Checks** - liveness and readiness probes
- **Security** - read-only root filesystem, security context
- **Load Balancing** - LoadBalancer service type
- **Persistent Storage** - PVC for MySQL

## 🛠️ Development

### Build Docker Image

```bash
docker build -t your-registry/your-app:latest .
```

