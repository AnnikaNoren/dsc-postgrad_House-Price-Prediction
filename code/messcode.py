
### Mess file code
# plotting the distribution of the target variable with a boxplot
plt.figure(figsize=(10,8))
sns.boxplot(x=df_final['SalePrice'])
plt.title("Boxplot for Target Variable")
plt.xlabel("Price in Dollars")
plt.savefig("./images/saleprice_boxplot_mess.png")
plt.show()

# plotting the correlation between variables and the target using a heatmap
plt.figure(figsize=(2,11))
sns.heatmap(df_final.corr()[['SalePrice']])
plt.title("Correlation of Each Independent Variable \n with the Target Variable \n")
plt.show()

plt.figure(figsize=(10,10))
sns.heatmap(X_train.corr())
plt.title("Exploring Correlation Between Features")
plt.show()