db = db.getSiblingDB('weather_alerts_db');  // Switch to the desired database

db.createUser({
    user: "monitorUser",
    pwd: "monitorPassword",
    roles: [
      { role: "clusterMonitor", db: "admin" },
      { role: "read", db: "local" }
    ]
  });
  
  db.createUser({
    user: "dataOperator",
    pwd: "securePassword",
    roles: [
      { role: "readWrite", db: "weather_alerts_db" }
    ]
});