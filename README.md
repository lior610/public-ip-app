# Public IP App — Flask + K8s + CI/CD via GitHub Actions & ArgoCD

This project is a Python and Flask-based app that shows the public IP of the client that sends the request.

---

## Full CI/CD Deployment

**Flow:**  
Python application → integration tests with `pytest` → built into Docker image → deployed with Helm → monitored and synced by ArgoCD → deployed to a remote Kubernetes cluster.

The Kubernetes cluster is a **k3s cluster** running on an **EC2 instance in AWS**.

The Helm chart includes the following objects:
1. A **Deployment** with 3 replicas of the pod, using the image tag deployed by GitHub Actions.
2. A **ClusterIP Service** that exposes port `5000` and routes traffic to port `5000` in the pod.
3. An **Ingress** (without host) that redirects traffic from port `80` to the service inside the cluster.  
   > **Note:** All of these values can be changed from the `values.yaml` file.

---

## CI/CD Pipeline (GitHub Actions)

The pipeline is defined in [`.github/workflows/ci-cd.yml`](./.github/workflows/ci-cd.yml).  
It consists of the following steps:

1. **Integration Test**  
   Runs with `pytest` to check that the site returns a valid response in both HTML and JSON format.

2. **Build**  
   Builds a Docker image using the `Dockerfile`. Pushes it to `lior610/public-ip` and tags it with `stable` and the GitHub run number (for versioning).

3. **Lint**  
   Uses `igabaydulin/helm-check-action@0.2.1` to run `helm lint` and `helm template`, to verify the Helm files work correctly.

4. **Deploy**  
   Updates the tag in `helm/values.yml`, which triggers ArgoCD to deploy the new version to the cluster.

---

## App Access

The app exposes the following endpoints:

- [`http://<ec2-public-ip>/`](http://<ec2-public-ip>/)  
  A simple web page showing the client's public IP.

- [`http://<ec2-public-ip>/json`](http://<ec2-public-ip>/json)  
  Returns a JSON response like: `{ "ip": "<External-IP>" }`

- [`http://<ec2-public-ip>/health`](http://<ec2-public-ip>/health)  
  Healthcheck endpoint for liveness probes.

---

## Process

1. Built the basic app in Python to return the public IP.
2. Created Docker manifests, including Deployment, Service, and Ingress.
3. Packaged everything with Helm and deployed on a local Minikube cluster.
4. Created build and deploy steps in GitHub Actions.
5. Created an EC2 instance running k3s to test whether the app correctly returns the external IP.
6. Debugged why, in the remote cluster, the IP shown was a Flannel network CIDR — and solved it.
7. Added integration tests and Helm checks to validate the files.
8. Final touches to the Helm chart — including resource limits and readiness/liveness probes.
9. Styled the HTML and CSS to improve the look of the site.

---

## Issues Occurred

1. **Public IP was not returned in remote cluster**

   After deploying to the remote k3s cluster, the app returned an internal pod IP (Flannel CIDR).  
   I initially assumed it was related to the Ingress controller and tried various deployment and configMap settings from online sources.  
   Then I checked using a NodePort service and still got the internal IP.  
   Eventually, I found that setting `externalTrafficPolicy: Local` in the service (or Ingress controller service) preserves the original IP by skipping SNAT — which is ideal for one-node clusters. After that, it worked.

2. **Notifications via email are hard to implement in GitHub Actions**

   GitHub sends default email notifications when the CI/CD pipeline fails.  
   I explored using Slack notifications with this action (But I wasn’t able to use it due to lack of a Slack account):

   ```yaml
   uses: rtCamp/action-slack-notify@v2
   env:
     SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
   ```