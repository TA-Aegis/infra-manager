CLUSTER_NAME=aegis
CLUSTER_URL=http://127.0.0.1:50308/

cluster-create:
	kind create cluster --name $(CLUSTER_NAME) --image kindest/node:v1.23.5 --config=kind.yaml
	kubectl config current-context
	kubectl create sa python

cluster-delete:
	kind delete cluster --name $(CLUSTER_NAME)
	kind delete clusters $(CLUSTER_NAME)
	kind delete cluster --name kind-$(CLUSTER_NAME)
	kind delete clusters kind-$(CLUSTER_NAME)

cluster-auth:
	TOKENS=$(kubectl describe sa python | grep Tokens | awk '{print $2}')
	@echo "export KIND_TOKEN=$(kubectl get secret $(TOKENS) -o json | jq -r .data.token | base64 --decode)" >> .env
	curl -k -X GET -H "Authorization: Bearer $KIND_TOKEN" $(CLUSTER_URL)apis
	kubectl apply -f ./k8s/service-account/

auth:
	@echo "KIND_TOKEN=$$(kubectl get secret $$(kubectl describe sa python | grep Tokens | awk '{print $$2}') -o json | jq -r .data.token | base64 --decode)" >> .env

env:
	@kubectl get secret $$(kubectl describe sa python | grep Tokens | awk '{print $$2}') -o json | jq -r .data.token | base64 --decode > .env.tmp
	@sed -i '' '/KIND_TOKEN/d' .env  # Delete the line containing "KIND_TOKEN"
	@echo "KIND_TOKEN=$$(cat .env.tmp)" >> .env  # Add the new line
	@rm .env.tmp

run:
	python src/main.py
