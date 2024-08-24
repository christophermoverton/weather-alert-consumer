db.createUser({
    user: "monitorUser",
    pwd: "monitorPassword",
    roles: [
      { role: "clusterMonitor", db: "admin" },
      { role: "read", db: "local" }
    ]
  });
  