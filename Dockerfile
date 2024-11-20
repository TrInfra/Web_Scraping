FROM minio/minio

ENV MINIO_ACCESS_KEY=${MINIO_ROOT_USER}
ENV MINIO_SECRET_KEY=${MINIO_ROOT_PASSWORD}

RUN mkdir -p /data && chmod -R 755 /data

ENTRYPOINT ["minio"]
EXPOSE 34219

CMD ["server", "/data", "--address", ":34219"]