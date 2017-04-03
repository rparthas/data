package ram.edu.twitterStorm.spout;

import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichSpout;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import org.apache.storm.utils.Utils;
import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;

import java.util.Map;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * Created by ram on 7/05/16.
 */
public class TweetSpout implements IRichSpout {

	LinkedBlockingQueue<String> queue = new LinkedBlockingQueue<String>();

	SpoutOutputCollector collector = null;

	class TweetListener implements StatusListener

	{

		public void onStatus(Status status) {
			queue.offer(status.getText());
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

	public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
		this.collector = collector;
		ConfigurationBuilder config = new ConfigurationBuilder().setOAuthConsumerKey("###")
				.setOAuthConsumerSecret("###").setOAuthAccessToken("###").setOAuthAccessTokenSecret("###");
		
		TwitterStreamFactory factory = new TwitterStreamFactory(config.build());
		TwitterStream stream = factory.getInstance();
		stream.addListener(new TweetListener());
		stream.sample();
	}

	public void close() {

	}

	public void activate() {

	}

	public void deactivate() {

	}

	public void nextTuple() {
		String ret = queue.poll();

		// if no tweet is available, wait for 50 ms and return
		if (ret == null) {
			Utils.sleep(50);
			return;
		}

		// now emit the tweet to next stage bolt
		collector.emit(new Values(ret));
	}

	public void ack(Object msgId) {

	}

	public void fail(Object msgId) {

	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("tweet"));
	}

	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}
