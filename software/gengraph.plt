set terminal png truecolor size 800,600
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S
set grid
set datafile separator ","
set output "genplot.png"
set format x "%H:%M\n%m/%d"
set y2tics
set ytics nomirror
set ylabel "Temperature in C or Humidity in %"
set y2label "Light level in Lux"
#set key autotitle columnhead
plot 'genplot.csv' using 1:2 axes x1y1 with histeps title "Temperature C" lt rgb "#f02000", \
     'genplot.csv' using 1:3 axes x1y1 with histeps title "Humidity"      lt rgb "#20f000", \
     'genplot.csv' using 1:4 axes x1y2 with histeps title "Lux"           lt rgb "#000000"
