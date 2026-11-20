pipeline {
    agent any
    environment {
        IMAGE_NAME = "pruebaciber-ev3-flask"
        CONTAINER_NAME = "pruebaciber-ev3-prod"
    }
    stages {
        stage('Construcción (Build)') {
            steps {
                echo 'Construyendo imagen Docker de pruebaciber-ev3...'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }
        stage('Pruebas (Test)') {
            steps {
                echo 'Ejecutando pruebas unitarias con pytest...'
                sh 'docker run --rm ${IMAGE_NAME}:latest pytest'
            }
        }
        stage('Despliegue (Deploy)') {
            steps {
                echo 'Desplegando aplicación en entorno de pruebas/producción...'
                sh 'docker stop ${CONTAINER_NAME} || true'
                sh 'docker rm ${CONTAINER_NAME} || true'
                sh 'docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:latest'
            }
        }
        stage('Pruebas de Seguridad (OWASP ZAP)') {
            steps {
                echo 'Ejecutando escaneo dinámico de seguridad con OWASP ZAP...'
                sh '''
                    sleep 3
                    docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "http://host.docker.internal:5000/hello?name=test" -r zap_report_vulnerable.html || true
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'zap_report_vulnerable.html', allowEmptyArchive: true
        }
    }
}