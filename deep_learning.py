# This program converts distances in kilometers
# to miles. The result is displayed in a label
# on the main window.
import tkinter
import h2o
from h2o.estimators import H2ORandomForestEstimator

h2o.shutdown
h2o.init(min_mem_size="10g", nthreads=-1)
class DRF_GUI:
    def __init__(self):
        # Create the main window.
        self.main_window = tkinter.Tk()
        # Create three frames to group widgets.
        self.top_frame = tkinter.Frame()
        self.mid_frame = tkinter.Frame()
        self.bottom_frame = tkinter.Frame()
        # Create the widgets for the top frame.
        self.prompt_label1 = tkinter.Label(self.top_frame,
                                          text='Number of trees:')
        self.ntrees_entry = tkinter.Entry(self.top_frame,
                                        width=10)
        # Create the widgets for the top frame.
        self.prompt_label2 = tkinter.Label(self.top_frame,
                                          text='Min_rows:')
        self.min_rows_entry = tkinter.Entry(self.top_frame,
                                        width=10)
        # Create the widgets for the top frame.
        self.prompt_label3 = tkinter.Label(self.top_frame,
                                          text='Max_Depth:')
        self.max_depth_entry = tkinter.Entry(self.top_frame,
                                        width=10)
        # Pack the top frame's widgets.
        self.prompt_label1.pack(side='left')
        self.ntrees_entry.pack(side='left')
        self.prompt_label2.pack(side='left')
        self.min_rows_entry.pack(side='left')
        self.prompt_label3.pack(side='left')
        self.max_depth_entry.pack(side='left')

        # Create the widgets for the middle frame.
        self.descr_label = tkinter.Label(self.mid_frame,
                                         text='AUC:')
        # Create the widgets for the middle frame.
        self.descr_label2 = tkinter.Label(self.mid_frame,
                                         text='LOGLOSS:')
        # We need a StringVar object to associate with
        # an output label. Use the object's set method
        # to store a string of blank characters.
        self.ntrees = tkinter.StringVar()
        self.min_rows = tkinter.StringVar()
        self.max_depth = tkinter.StringVar()
        self.auc = tkinter.StringVar()
        self.logloss = tkinter.StringVar()
        # Create a label and associate it with the
        # StringVar object. Any value stored in the
        # StringVar object will automatically be displayed
        # in the label.
        self.auc_label = tkinter.Label(self.mid_frame,
                                         textvariable=self.auc)
        self.logloss_label = tkinter.Label(self.mid_frame,
                                         textvariable=self.logloss)
        # Pack the middle frame's widgets.
        self.descr_label.pack(side='left')
        self.auc_label.pack(side='left')
        # Pack the middle frame's widgets.
        self.descr_label2.pack(side='left')
        self.logloss_label.pack(side='left')
        # Create the button widgets for the bottom frame.
        self.calc_button = tkinter.Button(self.bottom_frame,
                                          text='Calculate',
                                          command=self.calculate)
        self.auto_button = tkinter.Button(self.bottom_frame,
                                          text='Auto',
                                          command=self.auto)
        self.quit_button = tkinter.Button(self.bottom_frame,
                                          text='Quit',
                                          command=self.main_window.destroy)
        self.slider = tkinter.Scale(self.bottom_frame,
                                    from_=0,
                                    to=1,
                                    orient=tkinter.HORIZONTAL,
                                    resolution=0.1)
        # Pack the buttons.
        self.calc_button.pack(side='left')
        self.auto_button.pack(side='left')
        self.quit_button.pack(side='left')
        self.slider.pack(side='right')
        # Pack the frames.
        self.top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()
        # Enter the tkinter main loop.
        tkinter.mainloop()

    def auto(self):
        ntrees_loc = 400
        min_rows_loc = 10
        max_depth_loc = 9
        self.ntrees.set(ntrees_loc)
        self.min_rows.set(min_rows_loc)
        self.max_depth.set(max_depth_loc)
        # Import the titanic dataset into H2O:
        titanic = h2o.import_file("train.csv")
        test = h2o.import_file("test.csv")
        # Set the predictors and response;
        # set the response as a factor:
        titanic["Survived"] = titanic["Survived"].asfactor()
        predictors = ['Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']
        response = "Survived"
        # Split the dataset into a train and valid set:
        train, valid = titanic.split_frame(ratios=[.8], seed=1234)
        # Build and train the model:
        titanic_drf = H2ORandomForestEstimator(ntrees=ntrees_loc,
                                            max_depth=max_depth_loc,
                                            min_rows=min_rows_loc,
                                            calibrate_model=True,
                                            calibration_frame=valid,
                                            binomial_double_trees=True)
        titanic_drf.train(x=predictors,
                       y=response,
                       training_frame=train,
                       validation_frame=valid)
        # Eval performance:
        perf = titanic_drf.model_performance()
        # Generate predictions on a validation set (if necessary):
        pred = titanic_drf.predict(valid)
        #DODAC DO TESTOWYCH DANYCH W calculate() TEZ JEST
        pred2 = titanic_drf.predict(test)
        pred2.describe()
        test.describe()

        self.auc.set(perf.auc())
        self.logloss.set(perf.logloss())
        h2o.export_file(pred, 'result_pred.csv')
        h2o.export_file(pred2, 'result_pred2.csv')
       # print(pred2)
    # The convert method is a callback function for
    # the Calculate button.
    def calculate(self):
        # Get the value entered by the user into the
        # kilo_entry widget.
        ntrees_loc = int(self.ntrees_entry.get())
        min_rows_loc = int(self.min_rows_entry.get())
        max_depth_loc = int(self.max_depth_entry.get())
        self.ntrees.set(ntrees_loc)
        self.min_rows.set(min_rows_loc)
        self.max_depth.set(max_depth_loc)
        # Import the titanic dataset into H2O:
        titanic = h2o.import_file("train.csv")
        test = h2o.import_file("test.csv")
        # Set the predictors and response;
        # set the response as a factor:
        titanic["Survived"] = titanic["Survived"].asfactor()
        predictors = ['Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']
        response = "Survived"
        # Split the dataset into a train and valid set:
        ratio = float(self.slider.get())
        train, valid = titanic.split_frame(ratios=[ratio], seed=1234)
        # Build and train the model:
        titanic_drf = H2ORandomForestEstimator(ntrees=ntrees_loc,
                                            max_depth=max_depth_loc,
                                            min_rows=min_rows_loc,
                                            calibrate_model=True,
                                            calibration_frame=valid,
                                            binomial_double_trees=True)
        titanic_drf.train(x=predictors,
                       y=response,
                       training_frame=train,
                       validation_frame=valid)
        # Eval performance:
        perf = titanic_drf.model_performance()
        # Generate predictions on a validation set (if necessary):
        pred = titanic_drf.predict(valid)
        pred2 = titanic_drf.predict(test)

        self.auc.set(perf.auc())
        self.logloss.set(perf.logloss())
       # print(pred2)
        h2o.export_file(pred, 'result_pred.csv')
        h2o.export_file(pred2, 'result_pred2.csv')
# Create an instance of the KiloConverterGUI class.
drf_gui_01 = DRF_GUI()