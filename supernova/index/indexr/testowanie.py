__author__ = 'Kamil'
from websites.models import *
from index.func import *


def stworz_domene(nazwa="domena"):
    d = Domain(name=nazwa, pagerank=1)
    d.save()
    return d


def generuj_losowe_obeikty_webpage():
    dom = stworz_domene("lorem.com")
    con = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras semper aliquet sodales.
     Aliquam erat volutpat. Morbi rhoncus, sem nec pharetra fringilla, ante velit semper odio, lobortis vulputate neque
     lorem nec mi. Donec erat eros, sollicitudin non sagittis ut, accumsan rutrum tellus. Maecenas fermentum erat mi,
     vitae dignissim erat egestas nec. Ut consectetur lorem quis leo viverra consectetur. Integer ultrices faucibus ligula eget
      gravida. Nullam nec est nec mauris molestie maximus nec ac magna. Curabitur et ante euismod, lobortis lorem eu, tempor arcu.
      Pellentesque vitae dignissim urna, vel dignissim justo. Morbi at lacus at ante vulputate facilisis sit amet vitae turpis.
      Proin facilisis nec diam vel convallis.
     Quisque dapibus pulvinar ipsum, et varius turpis tempus nec. Aliquam non tellus vestibulum diam rutrum efficitur. """
    des="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    key="ala ma kota"
    titl="Ala ma kota!"
    pat="lorem.com/ala"

    w = Webpage(path=pat, title=titl, description=des, keywords=key, content=con, domain=dom)
    w.save()

    # wlasciwe testy

    # strona_do_zindeksowania(w)


