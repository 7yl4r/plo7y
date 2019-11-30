import pyflux as pf
import matplotlib.pyplot as plt
# %matplotlib inline


def plot(data, xname="value", exog_names=['seat_belt']):
    plt.figure(figsize=(15, 5))
    plt.plot(data.index, data[xname])
    plt.ylabel('Driver Deaths')
    plt.title('Deaths of Car Drivers in Great Britain 1969-84')
    plt.plot()

    model = pf.ARIMAX(
        data=data, formula=xname+'~1+seat_belt+oil_crisis',
        ar=1, ma=1, family=pf.Normal()
    )
    x = model.fit("MLE")
    x.summary()
    plt.show()
    model.plot_fit(figsize=(15, 10))
    model.plot_predict(
        h=10, oos_data=data.iloc[-12:], past_values=100, figsize=(15, 5)
    )
