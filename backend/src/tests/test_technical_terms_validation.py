"""
Tests for validating translation of technical terms and concepts in the TranslationService.
"""
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from uuid import UUID

from ..services.translation_service import TranslationService


class TestTechnicalTermsValidation:
    """Test class for validating translation of technical terms and concepts."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.translation_service = TranslationService()
        self.mock_db = Mock(spec=Session)
        self.chapter_id = UUID('12345678-1234-5678-1234-567812345678')

    def test_preservation_of_robotics_technical_terms(self):
        """Test that robotics-specific technical terms are preserved during translation."""
        original_content = """
In robotics, inverse kinematics (IK) is used to determine the joint parameters that achieve a desired position.
Forward kinematics (FK) calculates the position of the end effector based on joint angles.
ROS (Robot Operating System) is a flexible framework for writing robot software.
"""

        # Mock the translation to simulate a translation that preserves technical terms
        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            # Simulate a translation that would preserve technical terms
            mock_translate.return_value = """
روبوٹکس میں، معکوس کنیمیٹکس (IK) کا استعمال م joint parameters کا تعین کرنے کے لیے کیا جاتا ہے جو مطلوبہ پوزیشن حاصل کرے۔
فرورڈ کنیمیٹکس (FK) joint angles کی بنیاد پر end effector کی پوزیشن کا حساب لگاتا ہے۔
ROS (روبوٹ آپریٹنگ سسٹم) روبوٹ سافٹ ویئر لکھنے کے لیے ایک لچکدار ڈھانچہ ہے۔
"""
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that technical terms are preserved in their original form
            assert "IK" in result  # Should be preserved as acronym
            assert "FK" in result  # Should be preserved as acronym
            assert "ROS" in result  # Should be preserved as acronym
            assert "Robot Operating System" not in result  # Full form might be translated but acronym preserved

    def test_preservation_of_programming_concepts(self):
        """Test that programming concepts and code elements are preserved."""
        original_content = """
A PID controller is implemented with the following code:
```
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def compute(self, error):
        return self.kp * error + self.ki * integral + self.kd * derivative
```
The compute method calculates the control output.
"""

        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            mock_translate.return_value = """
ایک PID کنٹرولر درج ذیل کوڈ کے ساتھ نافذ کیا گیا ہے:
```
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def compute(self, error):
        return self.kp * error + self.ki * integral + self.kd * derivative
```
کمپیوٹ میتھڈ کنٹرول آؤٹ پٹ کا حساب لگاتا ہے۔
"""
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that code structure is preserved
            assert "class PIDController:" in result
            assert "def __init__" in result
            assert "def compute" in result
            assert "self.kp = kp" in result
            assert "return self.kp * error" in result

    def test_preservation_of_mathematical_formulas(self):
        """Test that mathematical formulas are preserved."""
        original_content = """
The equation for a robot's forward kinematics is:
T = R * d
Where T is the transformation matrix, R is rotation, and d is displacement.
"""

        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            mock_translate.return_value = """
روبوٹ کے فارورڈ کنیمیٹکس کے لیے مساوات یہ ہے:
T = R * d
جہاں T تبدیلی کا میٹرکس ہے، R ریٹیشن ہے، اور d برق آمیزی ہے۔
"""
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that mathematical expressions are preserved
            assert "T = R * d" in result  # Formula should remain unchanged
            assert "T" in result  # Variables should be preserved
            assert "R" in result
            assert "d" in result

    def test_preservation_of_sensor_names_and_units(self):
        """Test that sensor names and units are preserved."""
        original_content = """
The IMU (Inertial Measurement Unit) provides data in m/s² for acceleration.
LIDAR sensors measure distance in meters with precision up to 0.01m.
"""

        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            mock_translate.return_value = """
IMU (انیشل ناپ ساز) m/s² میں ایکسلریشن کے لیے ڈیٹا فراہم کرتا ہے۔
LIDAR سینسر میٹر میں 0.01m تک کی صحت کے ساتھ فاصلہ ناپتا ہے۔
"""
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that technical abbreviations and units are preserved
            assert "IMU" in result
            assert "LIDAR" in result
            assert "m/s²" in result  # Units should be preserved
            assert "m" in result  # Meters should be preserved

    def test_preservation_of_control_theory_terms(self):
        """Test that control theory terms are preserved."""
        original_content = """
In control theory, a system's stability is determined by its poles and zeros.
A PID controller adjusts the proportional (P), integral (I), and derivative (D) gains.
"""

        with patch.object(self.translation_service, 'translate_chapter_content') as mock_translate:
            mock_translate.return_value = """
کنٹرول تھیوری میں، ایک سسٹم کی استحکام اس کے poles اور zeros سے متعین ہوتی ہے۔
ایک PID کنٹرولر proportional (P)، integral (I)، اور derivative (D) gains کو ایڈجسٹ کرتا ہے۔
"""
            result = self.translation_service.translate_preserving_structure(
                original_content,
                "Urdu"
            )

            # Check that control theory terms are preserved
            assert "PID" in result
            assert "P" in result  # Individual letters in PID should be preserved
            assert "I" in result
            assert "D" in result
            assert "poles" in result  # Technical terms should be preserved
            assert "zeros" in result

    def test_translation_quality_with_technical_content(self):
        """Test quality validation with technical content."""
        original = "The Jacobian matrix J is used in robotics to relate joint velocities to end-effector velocities."
        translated = "Jacobian matrix J روبوٹکس میں joint velocities کو end-effector velocities سے متعلق کرنے کے لیے استعمال ہوتا ہے۔"

        # This should have good quality as technical terms are preserved
        quality = self.translation_service.validate_translation_quality(original, translated)
        assert quality > 0.5  # Should be above the 50% threshold

        # Test with poor quality translation (technical terms lost)
        poor_translation = "یہ ایک میٹرکس ہے جو کچھ چیزیں کرتی ہے۔"  # Vague, no technical terms
        poor_quality = self.translation_service.validate_translation_quality(original, poor_translation)
        assert poor_quality == 0.0  # Should be poor quality due to length and content


if __name__ == "__main__":
    pytest.main([__file__])