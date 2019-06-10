library(readxl)
library(reshape)
library(dummies)
library(qcc)


input_data = read.csv('~/Users/suvodeepmajumder/Downloads/repo.csv',header=TRUE, sep=",")

#input_data = input_data[which(input_data$Refactoring_type == 'Extract Method'),]
input_data = input_data[,-which(names(input_data) %in% c('Name','Type','Refactoring_type','Commit_hash'))]
#input_data = input_data[,which(names(input_data) %in% c('CountDeclInstanceVariable','CountDeclMethodPrivate','CountDeclMethodProtected','CountLineCodeExe','MaxInheritanceTree','Refactored'))]

input_data = dummy.data.frame(input_data)


train_size = 0.60
train_indices = sample(seq_len(nrow(input_data)), size = floor(train_size*nrow(input_data)))

train_data = input_data[train_indices,]
test_data = input_data[-train_indices,]

test_data.y = test_data[,which(names(test_data) %in% c('Refactored'))]
test_data.x = test_data[,-which(names(test_data) %in% c('Refactored'))]


fit.all <- glm(`Refactored` ~.,family=binomial(link='logit'),data=train_data, control = list(maxit = 500))

#fit.all <- glmnet(x, y, family = "binomial", alpha = 1, lambda = NULL)
coefs = fit.all$coefficients

significance_level = 0.05

coefs = summary(fit.all)$coefficients

significant_predictors = coefs[coefs[,4] < significance_level,]
print(summary(fit.all))

probas <- predict(fit.all,newdata = test_data.x,type='response')
predicted.classes <- ifelse(probas > 0.5, 1, 0)
observed.classes <- test_data[,which(names(test_data) %in% c('Refactored'))]
print(mean(predicted.classes == observed.classes))