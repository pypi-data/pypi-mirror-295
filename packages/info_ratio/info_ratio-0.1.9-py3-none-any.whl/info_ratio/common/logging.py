from loga import Loga

# all setup values are optional
loga = Loga(
    facility="info_ratio",  # name of program logging the message
    do_print=True,  # print each log to console
    truncation=1000,  # longest possible value in extra data
    private_data={"password"},  # set of sensitive args/kwargs
)
