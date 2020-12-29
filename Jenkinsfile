pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci
spec:
  containers:
    - name: docker
      image: docker/compose
      command:
        - cat
      tty: true
      volumeMounts:
        - mountPath: /var/run/docker.sock
          name: docker-sock
    - name: kubectl
      image: lachlanevenson/k8s-kubectl:v1.20.1
      command:
        - cat
      tty: true
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
  '''
    }
  }

  stages {
    stage('Build image') {
      steps {
        container('docker') {
          git url: 'https://github.com/it-muslim/quran-words.git'
          withCredentials([file(credentialsId: 'quran-words-production', variable: 'secretenv')])
          {
            sh "cp ${secretenv} ${WORKSPACE}/.env"
            sh 'docker-compose build'
            sh 'docker-compose push'
            stash name: "k8s", includes: "k8s/*"
          }
        }
      }

      post {
        success {
          echo 'Sucessfully dockerized containers'
        }

        failure {
          echo '> Docker Compose Building Failed ....'
          sh 'docker-compose down'
        }
      }
    }

    stage('Deploy') {
      steps {
        container('kubectl') {
          withKubeConfig([credentialsId: 'jenkins-account', serverUrl: 'https://91.121.210.90:16443']) {
            unstash 'k8s'
            sh 'kubectl rollout restart deployment django-deployment -n quran-words'
            sh 'kubectl delete -f ./k8s/frontend-job.yaml -n quran-words'
            sh 'kubectl create -f ./k8s/frontend-job.yaml -n quran-words'
          }
        }
      }
    }
  }
}
