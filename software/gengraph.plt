set terminal png size 800,600
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S
set grid
set datafile separator ","
set output "plot.png"
set format x "%H:%M\n%m/%d"
#set key autotitle columnhead
plot "ST54_6c_0e_80_80_86.csv" using 1:3 with histeps title columnhead lt rgb "#0080A0", \
     "ST54_6c_0e_80_80_86.csv" using 1:4 with histeps title columnhead lt rgb "#A08000", \
     "ST54_6c_0e_80_80_86.csv" using 1:5 with histeps title columnhead lt rgb "#80A000"
