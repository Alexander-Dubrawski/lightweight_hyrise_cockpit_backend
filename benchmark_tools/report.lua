done = function(summary, latency, requests)
    io.write("latency_values:\n")
    io.write(string.format('{"Min": %d, "Max": %d, "Avg": %d, "Stdev": %d}\n', latency.min, latency.max, latency.mean, latency.stdev))
    io.write("request_values:\n")
    io.write(string.format('{"Min": %d, "Max": %d, "Avg": %d, "Stdev": %d}\n', requests.min, requests.max, requests.mean, requests.stdev))
    io.write("latency_distribution:\n{")
    for _, p in pairs({50, 75.000, 90, 99.000, 99.900 ,99.990, 99.999 }) do
        n = latency:percentile(p)
        io.write(string.format('"%g%%": %d, ', p, n))
    end
    io.write(string.format('"%g%%": %d }\n', 99.999999999, latency:percentile(99.999999999)))
    percentiles = {} 
    for i=1, 99 do
        percentiles[i] = i
    end
    io.write("percentiles:\n")
    io.write('{"percentiles": [')
    for _, p in pairs(percentiles) do
        n = latency:percentile(p)
        io.write(string.format(" %d,",n))
    end
    io.write(string.format(" %d]}\n",latency:percentile(99.9999999)))
end

