import MQTT from "mqtt";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const client = await MQTT.connectAsync("mqtt://broker.hivemq.com");

const topic = "my/topic";

client.on("message", async (t, msg) => {
 if (t !== topic) return;
 console.log('received');

 try {
  const json = JSON.parse(msg);

  const res = await prisma.data
   .create({
    data: {
     timestamp: Date.now(),
     height: json.altitude,
     humidity: json.humidity,
     pressure: json.pressure,
     temperature: json.temperature,
    },
   });

 } catch {
  // not empty
 }
});

client.subscribe([topic], (e, g) => {
 if (e) throw e;
 console.log(g);
});