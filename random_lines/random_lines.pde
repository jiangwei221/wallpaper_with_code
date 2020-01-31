int num_kpts = 200;
int num_draws = 100;
ArrayList<PVector> keypoints;

void setup()
{
  size(4096, 2048);
  keypoints = new ArrayList<PVector>();
  for(int i=0; i<num_kpts; i++)
  {
    PVector point = new PVector(random(0, width/2), random(0, height));
    keypoints.add(point);
  }
  smooth();
  noLoop();
}

void draw()
{
  for(int i=0; i<num_draws; i++)
  {
    for(int j=0; j<num_kpts; j++)
    {
      pushMatrix();
      PVector point = keypoints.get(j);
      translate(point.x+random(0, 20), point.y+random(0, 20));
      rotate(TWO_PI * random(0, 1));
      stroke(0, 0, 0, 10);
      line(-10000, 0, 10000, 0);
      popMatrix();
    }
  }
  save("lines.png");
}
