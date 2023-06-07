### Question 2: Software Engineering

#### Describe all steps in the development cycle (from zero to production)
1. Data Collection and Pre-processing: Since all models need data, the first step is to collect them. This could involve web scraping, accessing APIs, or querying databases. The collected data is then cleaned and transformed into a suitable format.

2. Protyping: Here we build a protyping model to verify if the problem can be solved effectively with ML. Different algorithms are tried and the results are compared. This step is repeated until a satisfactory model is found.

3. Model Development:
Model Development: The best performing model from the prototyping stage is further fine-tuned. This could involve hyperparameter optimization, feature engineering, or other techniques to improve model performance.

4. Code development: Now we need to automate the pipeline, to speedup the process and make it reproducible. This involves writing code for data preprocessing/collection automation, automating model training and evalution.

5. Testing: This should be done throught the whole process, but it's especially important during the code development phase. This ensures that the code is working as expected and model performance is not degraded.

6. Deployment: The software is deployed using a CI/CD pipeline. This usually involves configuring of cloud servers/kubernetes clusters. From model point, this usually means serving the model and it's api endpoint.

7. Maintanance: This is a continuous phase espececially from in ML projects. The model needs to be retrained periodically to keep up with the changing data. The model also needs to be monitored to ensure that everything is working as expected.

#### Necessary Tools:

1. Data Collection and Processing: Python + pandas/spark based on the size of the data. For webscraping one can use beautifulsoup or scrapy.
2. Model Development: Python with scikit-learn for classical ML or Tensorflow/PyTorch/Hugging face for deep learning.
3. Code Development: for API I would use Flask, otherwise it depends on the use case. Since we run stuff in cloud, it's good idea to check the offerings for DBs or
data managment tools from the cloud provider. Usually they provide managed spark clusters, which can be used for data processing.
4. CI/CD: Since we are on cloud we probably going to use the providers CI/CD tools (e.g. AWS AzurePipeline).
5. Testing: PyTest/unittest for Python
6. Deployment: Kubernetes for container orchestration, or one can use teraform to manage the cloud infrastructure (not much experience with teraform though).


#### Best practices for committing code/feature into a repository:
- Commit more often rather than less often. This makes it easier to track down bugs and revert changes if necessary. Nobody wants to see 1k LOC commits.
- Provide good description on PRs and commits.
- Some people recommend squashing before merging, but I never found an advantage in that.
- Each new feature should have it's own branch.
- Running minimal tests before code is merged.
- Precommit hooks to ensure that code is formatted correctly and passes minimal tests.

#### Types of Tests:
- Unit Tests: Testing individual compnents of the software in isolation. These are easy to automate. Runs in CI/CD pipeline before merging and locally before committing.
- Integration Tests: Tests the interaction between different components of the software. A bit harder to automate, we can use Selenium for web apps. Staging environment is used for these tests.
- Performance Tests: Tests the speed and scalability of the software. This is done in staging environment.

#### How to ensure that the code is working as expected:
- Unit tests
- Content Itegration/Delivery Pipeline (CI/CD)
- Data Collection
- Monitoring

#### Describe how you would deal with silos in teams/members of the team
- Try to push the communication more. Out of work activities, team building activities, etc.
- Pair programming can be used to share knowledge and build trust.
- Less restricts on each others work. E.g. data scientists should be able to write code and data engineers should be able to do some data analysis.

#### Describe optimal team/workflow based on your experience.
- I don't think that having too seprate roles is good idea. E.g. data scientists and data engineers should try to learn from each other.
- Being a bit agile. It's really hard to work towards goal x for 6 months and then realize that it's not what the customer wants. So it's better to have shorter iterations and get feedback from the customer.
- Sharing knowledge between teams.
