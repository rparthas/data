package ram.edu.twitterStorm.bolt;

import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

public class ParseTweetBolt implements IRichBolt {

	OutputCollector collector = null;

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		this.collector = collector;

	}

	public void execute(Tuple input) {
		String tweet = input.getStringByField("tweet");
		if (tweet != null && tweet.contains("#")) {
			String subTweet = tweet.substring(tweet.indexOf("#"), tweet.length());
			String hashTag = subTweet.split(" ")[0];
			collector.emit(new Values(hashTag));
		} else {
			return;
		}

	}

	public void cleanup() {
		// TODO Auto-generated method stub

	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("hashTag"));

	}

	public Map<String, Object> getComponentConfiguration() {
		// TODO Auto-generated method stub
		return null;
	}

}
