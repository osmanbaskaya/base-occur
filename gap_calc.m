PATH = '/home/tyr/playground/base-occur/vectors/original/';

files = dir('/home/tyr/playground/base-occur/corpus/original/');
f = fopen('word-cluster_k.txt', 'w');
max_k = 10;
tic
for i=3:length(files)
    filename = files(i).name;
    disp(filename);
    X = csvread(strcat(PATH, filename, '.vec')); % word name
    [opt_k, max_gap] = gap_statistics(X, 1:max_k, 10, 0);
    fprintf(f, '%s ', filename); 
    fprintf(f, '%d %d\n', opt_k, max_gap);
end


fclose(f);
toc