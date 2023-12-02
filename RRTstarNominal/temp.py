import numpy as np

def calculate_signed_angle(p1, p2, p3):
    """
    Calculate the signed angle at p2 formed by the line segments p1-p2 and p2-p3.
    
    Args:
    p1, p2, p3 (tuples/lists): Coordinates of the three points (x, y).

    Returns:
    float: Signed angle at p2 in degrees. Positive if the angle is counterclockwise,
           negative if clockwise.
    """
    # Convert points to numpy arrays for vector operations
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # Calculate vectors
    v1 = p1 - p2
    v2 = p3 - p2

    # Calculate the angle using the dot product and arccosine function
    angle_radians = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))

    # Calculate the cross product to determine the direction of the angle
    cross_product = np.cross(v1, v2)

    # Convert to degrees and apply sign based on the direction
    if cross_product > 0:
        # Counterclockwise direction
        angle_degrees = np.degrees(angle_radians)
    else:
        # Clockwise direction
        angle_degrees = -np.degrees(angle_radians)

    return angle_degrees

# Example usage
p1 = (1, 2)
p2 = (2, 1)
p3 = (3, 2)

signed_angle = calculate_signed_angle(p1, p2, p3)
print(signed_angle)