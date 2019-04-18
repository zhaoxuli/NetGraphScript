data <- readRDS('D:/Play_Ground/Task-play/Lab3/chinese_sociologist.RDS');
node_info = data[[9]][[3]];
print (names(node_info));
write.table(node_info,"Source_data_new.csv",sep=',',quote = FALSE,row.names = FALSE,col.names = FALSE)
