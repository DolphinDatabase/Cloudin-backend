{{- define "cloudin-midall.probeAndResources" -}}
livenessProbe:
  httpGet:
    path: /
    port: {{ . }}
readinessProbe:
  httpGet:
    path: /
    port: {{ . }}
resources:
  limits:
    cpu: 100m
    memory: 256Mi
  requests:
    cpu: 80m
    memory: 128Mi
{{- end -}}

{{- define "cloudin-midall.getImage" -}}
{{- $imageName := .Values.backend.image.repository -}}
{{- $tag := .Values.backend.image.tag -}}
{{- printf "%s:%s" $imageName $tag -}}
{{- end -}}

{{- define "cloudin-midall.image" -}}
- name: backend
  image: {{ include "cloudin-midall.getImage" . }}
  ports:
    - containerPort: {{ .Values.backend.ports.containerPort }}
  env:
  - name: DATABASE_URL
    value: "mysql://dbuser:dbuser@cloudin-midall-mysql:3306/cloudin"
{{- end -}}