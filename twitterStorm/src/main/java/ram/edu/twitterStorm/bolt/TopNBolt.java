package ram.edu.twitterStorm.bolt;

import java.util.Calendar;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import ram.edu.twitterStorm.util.Util;

public class TopNBolt implements IRichBolt {

	long start = 0;
	long frequency = 0;
	int topN = 0;

	Map<String, Integer> map = new LinkedHashMap<String, Integer>();
	OutputCollector collector = null;

	public TopNBolt(long frequency, int topN) {
		this.frequency = frequency;
		this.topN = topN;
	}

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		this.collector = collector;
	}

	private void reset() {
		start = Calendar.getInstance().getTimeInMillis();
	}

	public void execute(Tuple input) {
		String hashTag = input.getStringByField("hashTag");
		int count = input.getIntegerByField("count");
		if (start == 0)
			start = Util.reset();
		if (map.containsKey(hashTag)) {
			map.put(hashTag, map.get(hashTag) + count);
		} else {
			map.put(hashTag, count);
		}

		if (Util.getDiff(start) > frequency && map.size() > topN) {
			int counter = topN;
			TreeMap<Integer, List<String>> treeMap = Util.sortMap(map);
			while (counter > 0) {
				Entry<Integer, List<String>> last = treeMap.lastEntry();
				for (String keys : last.getValue()) {
					counter--;
					collector.emit(new Values(keys));
				}
				treeMap.remove(last.getKey());
			}
			reset();
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