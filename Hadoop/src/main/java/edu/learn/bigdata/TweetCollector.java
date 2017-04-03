package edu.learn.bigdata;

import java.util.Properties;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;

import twitter4j.HashtagEntity;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;
import twitter4j.conf.ConfigurationBuilder;

public class TweetCollector {

	private Producer<String, String> producer;
	private String topicName;
	TweetListener tweetListener = new TweetListener();

	public static void main(String[] argv) throws Exception {

		// Configure the Producers
		Properties configProperties = new Properties();
		configProperties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
		configProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
				"org.apache.kafka.common.serialization.ByteArraySerializer");
		configProperties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
				"org.apache.kafka.common.serialization.StringSerializer");

		TweetCollector tc = new TweetCollector();
		tc.topicName = "tweets";
		tc.producer = new KafkaProducer<String, String>(configProperties);
		ConfigurationBuilder config = new ConfigurationBuilder().setOAuthConsumerKey("##")
				.setOAuthConsumerSecret("##")
				.setOAuthAccessToken("48344566-##")
				.setOAuthAccessTokenSecret("##");

		TwitterStreamFactory factory = new TwitterStreamFactory(config.build());
		TwitterStream stream = factory.getInstance();
		stream.addListener(tc.tweetListener);
		stream.sample();
	}

	class TweetListener implements StatusListener

	{

		public void onStatus(Status status) {
			if (status.getHashtagEntities() != null) {
				for (HashtagEntity he : status.getHashtagEntities()) {
					ProducerRecord<String, String> rec = new ProducerRecord<String, String>(topicName, he.getText());
					producer.send(rec);
				}
			}

		}

		public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {

		}

		public void onTrackLimitationNotice(int numberOfLimitedStatuses) {

		}

		public void onScrubGeo(long userId, long upToStatusId) {

		}

		public void onStallWarning(StallWarning warning) {

		}

		public void onException(Exception ex) {

		}
	}

}
