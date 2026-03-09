DYNAMICS = {
    "PP": 10,
    "P": 30,
    "MP": 50,
    "MF": 70,
    "F": 90,
    "FF": 110
}

class Dynamics:
    """
    Handles dynamics for a phrase/measure.
    Most phrases are stable, some have cresc/decresc.
    """

    def __init__(self, rng, start_velocity=None, end_velocity=None, curve="linear", noise_range=2, change_prob=0.2):
        self.rng = rng
        self.curve = curve
        self.noise_range = int(noise_range)
        self._noise_values = list(range(-self.noise_range, self.noise_range + 1))
        self.change_prob = change_prob

        if start_velocity is None:
            self.start_velocity = self._choose_random_dynamic()
        else:
            self.start_velocity = start_velocity

        if end_velocity is None:
            change_choices = [True] * int(change_prob*10) + [False] * int((1-change_prob)*10)
            do_change = self.rng.choice(change_choices)
            if do_change:
                self.end_velocity = self._choose_random_dynamic()
            else:
                self.end_velocity = self.start_velocity
        else:
            self.end_velocity = end_velocity

    def _choose_random_dynamic(self):
        index = self.rng.choice(list(range(len(DYNAMICS))))
        return list(DYNAMICS.values())[index]

    def choose(self, position=0.0):
        """
        Choose velocity for a note at relative position in phrase
        """
        if self.curve == "linear":
            base = self.start_velocity + int(position * (self.end_velocity - self.start_velocity))
        elif self.curve == "random":
            lower = min(self.start_velocity, self.end_velocity)
            upper = max(self.start_velocity, self.end_velocity)
            base = self.rng.choice(list(range(lower, upper + 1)))
        else:
            base = self.start_velocity

        noise = self.rng.choice(self._noise_values)
        velocity = max(0, min(127, base + noise))
        return velocity
    
    @classmethod
    def accent_boost(self, pos):
        """
        Returns a velocity boost depending on rhythmic position.
        pos = 0..1 in the bar
        """
        eps = 0.01

        if abs(pos - 0.0) < eps:
            return 12
        if abs(pos - 0.5) < eps:
            return 8
        if abs(pos - 0.25) < eps:
            return 4
        if abs(pos - 0.75) < eps:
            return 4

        return 0