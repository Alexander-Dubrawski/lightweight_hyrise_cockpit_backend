done = function(summary, latency, requests)
    io.write("latency_values:\n")
    io.write(
        string.format(
            '{"Min": %.3f, "Max": %.3f, "Avg": %.3f, "Stdev": %.3f}\n', 
            (latency.min / 1000), 
            (latency.max/ 1000), 
            (latency.mean/ 1000), 
            (latency.stdev/ 1000)
            )
        )
    io.write("request_values:\n")
    io.write(
        string.format(
            '{"Min": %d, "Max": %d, "Avg": %d, "Stdev": %d}\n', 
            requests.min, 
            requests.max, 
            requests.mean, 
            requests.stdev
            )
        )
    io.write("latency_distribution:\n{")
    for _, p in pairs({1, 25, 50, 75, 90, 99, 99.9 }) do
        n = latency:percentile(p)
        io.write(string.format('"%g%%": %.3f, ', p, (n / 1000)))
    end
    io.write(string.format('"%g%%": %.3f }\n', 99.99, (latency:percentile(99.99) / 1000)))
    percentiles = {} 
    for i=1, 99 do
        percentiles[i] = i
    end
    io.write("percentiles:\n")
    io.write('{"percentiles": [')
    for _, p in pairs(percentiles) do
        n = latency:percentile(p)
        io.write(string.format(" %.3f,",(n / 1000)))
    end
    io.write(string.format(" %.3f]}\n", (latency:percentile(99.9999999) / 1000)))
end

