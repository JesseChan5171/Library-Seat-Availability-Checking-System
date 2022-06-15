from matplotlib import pyplot as plt
import cv2
import numpy as np
import time


def show_img(img):
    cv2.namedWindow('ImageShow', cv2.WINDOW_NORMAL)
    cv2.imshow("ImageShow", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread("demo_room.png")
# img = cv2.circle(img, (160,180), radius=7, color=(0, 0, 255), thickness=-1)
# img = cv2.circle(img, (300,400), radius=7, color=(0, 0, 255), thickness=-1)

count = 0
l = [230, 300, 380]
lx = np.arange(160, 300, 20)

occ = []
plot_y = []

print(lx)
print(l)

wh_ch = len(l)*len(lx)
print(wh_ch)
np.random.seed(4)
while True:

    x = np.random.choice(lx)
    y = np.random.choice(l)

    if [x, y] in occ:
        continue
    else:
        occ.append([x, y])

    num = np.random.randint(0, 10)
    # Random process
    if num == 9:
        # No Mask; Red point
        print("Drew Red", x, y)
        img = cv2.circle(img, (x, y), radius=7,
                         color=(0, 0, 255), thickness=-1)
        count += 1
    else:
        # Mask; Green point
        print("Drew Green", x, y)
        img = cv2.circle(img, (x, y), radius=7,
                         color=(0, 255, 0), thickness=-1)
        count += 1

    if num >= 7 and occ:
        lex, ley = occ[0]
        img = cv2.circle(img, (lex, ley), radius=7,
                         color=(255, 255, 255), thickness=-1)
        occ.remove([lex, ley])
        count -= 1
    if num >= 9 and occ:
        lex, ley = occ[0]
        img = cv2.circle(img, (lex, ley), radius=7,
                         color=(255, 255, 255), thickness=-1)
        occ.remove([lex, ley])
        count -= 1
    print("Total people: ", count)
    print("Coordinate:", occ)

    plot_y.append(len(occ))

    img_te = img.copy()
    cv2.putText(img_te, "Number of people: " + str(count), (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # IF room full
    if count == wh_ch:
        cv2.putText(img_te, "Study room 1 is Full", (30, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        break

    # Show image
    cv2.imshow('frame', img_te)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if count == wh_ch:
        time.sleep(100000)
    # time.sleep(np.random.exponential(2))
    time.sleep(1)


# Close image
print("Simulation Done")
cv2.waitKey(1)
cv2.destroyAllWindows()

x = np.arange(len(plot_y), step=1)

# Plot graph
plt.plot(x, plot_y)
plt.show()
