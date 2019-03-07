package fiduciagad.de.sft.mqtt;

import java.io.Closeable;

import org.eclipse.paho.client.mqttv3.IMqttClient;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.eclipse.paho.client.mqttv3.MqttSecurityException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Setup implements Closeable {

	private final IMqttClient mqttClient;

	public Setup(String host, int port) throws MqttSecurityException, MqttException {
		mqttClient = makeMqttClient(host, port);

	}

	public void close() {
		try {
			this.mqttClient.disconnect();
			this.mqttClient.close();
		} catch (MqttException e) {
			throw new RuntimeException(e);
		}
	}

	private IMqttClient makeMqttClient(String host, int port) throws MqttException, MqttSecurityException {
		IMqttClient client = new MqttClient("tcp://" + host + ":" + port, "SetupClient", new MemoryPersistence());
		client.connect();
		return client;
	}

	public void sendIdle(String string) throws MqttPersistenceException, MqttException {

		mqttClient.publish("idle", string.getBytes(), 0, false);

	}

	public void sendScore(String string) throws MqttPersistenceException, MqttException {
		
		
		
		mqttClient.publish("score", string.getBytes(), 0, false);
		
	}

}