# movies-recommendation-engine
This project includes an engine that identifies _similar movies_ using different similarity matrix. It uses _MapReduce jobs_ on _Hadoop cluster(s)_ to compute similarities in movies dataset.

#### Running Instructions
Refer command line running instructions included in python scripts.

#### Setup Guidelines

###### A. MRJob Setup
 1. Install mrjob with _pip_
```sh
$ pip install mrjob
```

or from ```git``` clone the [source code:](https://github.com/yelp/mrjob)

```sh
$ python setup.py test && python setup.py install
```
2. You can Test your installation by writing a sample job from this [example](https://pythonhosted.org/mrjob/guides/quickstart.html#installation).
3. For more information about ```mrjob```, read documentation [here](https://pythonhosted.org/mrjob/).

###### B. MovieLens Dataset Download
I am using _MovieLens Dataset_ for this project. You can download the dataset from this [link](http://grouplens.org/datasets/movielens/).
- MovieLens 100K Dataset
- MovieLens 1M Dataset

_Note: Larger datasets of 10M and 20M movie reviews are also available._

###### C. AWS Setup
1. Create an _AWS_ Account or login to your existing account.
2. Set below 2 environment variables on your local machine. Get these keys from ```Security Credentials > Access Keys``` on _AWS_:
  - _AWS_ACCESS_KEY_ID_
  - _AWS_SECRET_ACCESS_KEY_
3. Restart your _Terminal_.

#### License

**Free Software**

