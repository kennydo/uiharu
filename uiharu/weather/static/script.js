$(document).ready(function() {
    var currentTimeInSeconds = new Date().getTime() / 1000;
    var graphStartTime = Math.round(currentTimeInSeconds - (60 * 60 * 24 * 30));

    var xScale = new Plottable.Scales.Time();
    var yScale = new Plottable.Scales.Linear();
    var colorScale = new Plottable.Scales.Color();

    var xAxis = new Plottable.Axes.Time(xScale, "bottom");
    var yAxis = new Plottable.Axes.Numeric(yScale, "left");
    var yLabel = new Plottable.Components.AxisLabel("Temperature (ºF)", -90);

    var legend = new Plottable.Components.Legend(colorScale).maxEntriesPerRow(3);
    var plots = new Plottable.Components.Group();

    var table = new Plottable.Components.Table([
        [null, legend],
        [yAxis, plots],
        [null, xAxis]
    ]);

    table.renderTo("svg#weather");

    d3.json("/api/v1/sensors/taroumaru/measurements?start_time=" + graphStartTime, function(error, data) {
        var plot = new Plottable.Plots.Line();
        data = data.measurements;

        plot.x(function(d) { return d.timestamp * 1000; }, xScale)
            .y(function(d) { return d.value; }, yScale)
            .addDataset(new Plottable.Dataset(data));

        plots.append(plot);
    });

});
