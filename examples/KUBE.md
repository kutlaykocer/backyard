# start kubernetes
cd deployments/kubernetes/secrets
kubectl apply -f .

# Start dashboard
Link: https://www.ntweekly.com/2018/05/25/deploy-kubernetes-web-ui-dashboard-docker-windows/
kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
kubectl proxy
firefox http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

# Start other services
cd deployments/kubernetes
kubectl apply -f pvc.yaml
kubectl apply -f gridfs.yaml
kubectl apply -f nats-conf.yaml
kubectl apply -f nats.yaml

# Access service via localhost
kubectl get pods
kubectl port-forward nats-0 4222


# Mongodb
mkdir db
mongod -dpath db
mongo

# NATS
gnatsd
