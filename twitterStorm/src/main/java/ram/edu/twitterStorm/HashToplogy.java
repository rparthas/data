package ram.edu.twitterStorm;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;
import org.apache.storm.utils.Utils;

import ram.edu.twitterStorm.bolt.CountBolt;
import ram.edu.twitterStorm.bolt.ParseTweetBolt;
import ram.edu.twitterStorm.spout.TweetSpout;

/**
 * Main Class for Creating topology and running
 */
public class HashToplogy {
	public static void main(String[] args) {

		LocalCluster cluster = new LocalCluster();

		TopologyBuilder builder = new TopologyBuilder();
		builder.setSpout("tweetSpout", new TweetSpout(), 1);
		builder.setBolt("parseTweetBolt", new ParseTweetBolt(), 10).shuffleGrouping("tweetSpout");
		//builder.setBolt("rollingCountBolt", new RollingCountBolt(20000), 15).fieldsGrouping("parseTweetBolt",
		//		new Fields("hashTag"));
		//builder.setBolt("topNBolt", new TopNBolt(100000,10)).globalGrouping("rollingCountBolt");
		//builder.setBolt("reportBolt", new ReportBolt()).globalGrouping("topNBolt");
		builder.setBolt("countBolt", new CountBolt()).fieldsGrouping("parseTweetBolt",new Fields("hashTag"));
		Config conf = new Config();
		conf.setDebug(false);
		conf.setNumWorkers(20);
		cluster.submitTopology("hashTopology", conf, builder.createTopology());
		Utils.sleep(1000000);
		cluster.killTopology("hashTopology");
		cluster.shutdown();
	}
}
