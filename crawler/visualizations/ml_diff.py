from crawler.database_parser import masterylevel_by_role
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect('../games.db')
    cursor = conn.cursor()
    j,m,t,jj,mm,tt = masterylevel_by_role(cursor)
    conn.close()
    j_diff = np.array(jj)- np.array(j)
    m_diff = np.array(mm) - np.array(m)
    t_diff = np.array(tt) - np.array(t)

    print(np.mean(j_diff), np.mean(m_diff), np.mean(t_diff))

    #plt.plot(np.sort(j_diff))
    #plt.plot(np.sort(m_diff))
    #plt.plot(np.sort(t_diff))

    plt.boxplot(np.vstack((j_diff, m_diff, t_diff)).transpose(), 0, '')


    plt.show()