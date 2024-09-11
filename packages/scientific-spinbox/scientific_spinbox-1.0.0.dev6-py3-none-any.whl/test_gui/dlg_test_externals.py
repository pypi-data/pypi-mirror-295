from qtpy import QtWidgets
from decimal import Decimal, setcontext

from scientific_spinbox.widget import ScientificSpinBox
from test_gui.ui.dlg_testspinbox_externals import Ui_Dialog as Ui_TestSpinBoxExternalsDialog

class TestExternalsDialog(QtWidgets.QDialog):
    """
    Dialog that shows ScientificSpinBox and some external test controls.

    Used to test the behaviour of the ScientificSpinBox.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_TestSpinBoxExternalsDialog()

        # Configures Ui
        self.ui.setupUi(self)

        self._controls = {
            'thousand_separators': True,
            'default_decimals': 2,
            'default_value': 0.000,
            'display_unit': 'ms',
            'enable_tooltip': True,
            'base_unit': 'us',
            'allowed_units': None,
            'preferred_units': None
        }

        self.scientificSpinBox = ScientificSpinBox(
            **self._controls,
            parent=self.ui.testSpinBox1.parentWidget()
        )

        # Replaces necessary widgets
        self.ui.testSpinBox1.parentWidget().layout().replaceWidget(
            self.ui.testSpinBox1,
            self.scientificSpinBox
        )
        self.ui.testSpinBox1 = self.scientificSpinBox
        setcontext(self.scientificSpinBox.backend.decimalsContext)

        # Connect apply button
        self.ui.applyButton.clicked.connect(self.applyControls)

        # Connect externals buttons
        self.ui.setValueFloatButton.clicked.connect(self.onSetValueFloatSlot)
        self.ui.setValueDecimalButton.clicked.connect(self.onSetValueDecimalSlot)
        self.ui.setDecimalsButton.clicked.connect(self.onSetDecimalsChangeSlot)

        # Set defaults
        self.ui.displayUnitTextEdit.setText(self._controls['display_unit'])
        self.ui.baseUnitTextEdit.setText(self._controls['base_unit'])
        self.ui.defaultDecimalsTextEdit.setText(str(self._controls['default_decimals']))
        self.ui.defaultValueTextEdit.setText(str(self._controls['default_value']))
        self.ui.preferredUnitsTextEdit.setText(self._controls['preferred_units'])

        self.ui.setValueFloatTextEdit.setText(str(self._controls['default_value']))
        self.ui.setValueDecimalTextEdit.setText(str(self._controls['default_value']))
        self.ui.setDecimalsTextEdit.setText(str(self._controls['default_decimals']))

        # Connect controls and labels
        self.connectSlots()
        self.onValueChangeSlot()
        return

    def connectSlots(self):
        # Text edits
        self.ui.displayUnitTextEdit.textChanged.connect(self.onDisplayUnitChangeSlot)
        self.ui.baseUnitTextEdit.textChanged.connect(self.onBaseUnitChangeSlot)
        self.ui.defaultDecimalsTextEdit.textChanged.connect(self.onDefaultDecimalsChangeSlot)
        self.ui.defaultValueTextEdit.textChanged.connect(self.onDefaultValueChangeSlot)
        self.ui.allowedUnitsTextEdit.textChanged.connect(self.onAllowedUnitsChangeSlot)
        self.ui.preferredUnitsTextEdit.textChanged.connect(self.onPreferredUnitsChangeSlot)

        # Check boxes
        self.ui.thousandSepCheckBox.stateChanged.connect(self.onThousandSepEnableChangeSlot)
        self.ui.tooltipCheckBox.stateChanged.connect(self.onTooltipEnableChangeSlot)
        self.ui.integerRoundCheckBox.stateChanged.connect(self.onIntegerRoundCheckBoxChangeSlot)

        self.scientificSpinBox.valueChanged.connect(self.onValueChangeSlot)
        self.scientificSpinBox.textChanged.connect(self.onTextChangeSlot)
        self.onIntegerRoundCheckBoxChangeSlot()
        return
    
    def onSetValueFloatSlot(self):
        text = self.ui.setValueFloatTextEdit.toPlainText()
        if text:
            try:
                value = float(text)
                self.scientificSpinBox.setValue(value)
            except Exception:
                return
            
    def onSetValueDecimalSlot(self):
        text = self.ui.setValueDecimalTextEdit.toPlainText()
        if text:
            try:
                value = Decimal(text)
                self.scientificSpinBox.setValue(value)
            except Exception:
                return
            
    def onSetDecimalsChangeSlot(self):
        text = self.ui.setDecimalsTextEdit.toPlainText()
        if text:
            try:
                decimals = int(text)
                self.scientificSpinBox.setDecimals(decimals)
            except Exception:
                return
    
    def onPreferredUnitsChangeSlot(self):
        if self.ui.preferredUnitsTextEdit.toPlainText():
            self._controls['preferred_units'] = self.ui.preferredUnitsTextEdit.toPlainText().split(',')
    
    def onIntegerRoundCheckBoxChangeSlot(self):
        if self.ui.integerRoundCheckBox.isChecked():
            self._controls['allowed_units'] = None
            self._controls['display_unit'] = None

            # Disable displayUnit
            self.ui.displayUnitTextEdit.setText('')
            self.ui.displayUnitTextEdit.setDisabled(True)

            # Disable allowedUnits
            self.ui.allowedUnitsTextEdit.setText('')
            self.ui.allowedUnitsTextEdit.setDisabled(True)

            # Enable preferredUnits
            self.ui.preferredUnitsTextEdit.setDisabled(False)
        else:
            # Disable preferredUnits
            self._controls['preferred_units'] = None
            self.ui.preferredUnitsTextEdit.setDisabled(True)

            # Enable allowedUnits and displayUnits
            self.ui.allowedUnitsTextEdit.setDisabled(False)
            self.ui.displayUnitTextEdit.setDisabled(False)

    
    def onDefaultValueChangeSlot(self):
        if self.ui.defaultValueTextEdit.toPlainText():
            self._controls['default_value'] = float(self.ui.defaultValueTextEdit.toPlainText())

    def onDefaultDecimalsChangeSlot(self):
        if self.ui.defaultDecimalsTextEdit.toPlainText():
            self._controls['default_decimals'] = int(self.ui.defaultDecimalsTextEdit.toPlainText())
    
    def onAllowedUnitsChangeSlot(self):
        if self.ui.allowedUnitsTextEdit.toPlainText():
            self._controls['allowed_units'] = self.ui.allowedUnitsTextEdit.toPlainText().split(',')

    def onTooltipEnableChangeSlot(self):
        self._controls['enable_tooltip'] = self.ui.tooltipCheckBox.isChecked()

    def onThousandSepEnableChangeSlot(self):
        self._controls['thousand_separators'] = self.ui.thousandSepCheckBox.isChecked()

    def onDisplayUnitChangeSlot(self):
        if self.ui.displayUnitTextEdit.toPlainText():
            self._controls['display_unit'] = self.ui.displayUnitTextEdit.toPlainText()
        else:
            self._controls['display_unit'] = None

    def onBaseUnitChangeSlot(self):
        self._controls['base_unit'] = self.ui.baseUnitTextEdit.toPlainText()
        
    def applyControls(self):
        print(self._controls)
        self.scientificSpinBox = ScientificSpinBox(
            **self._controls,
            parent=self.ui.testSpinBox1.parentWidget()
        )

        # Replaces necessary widgets
        self.ui.testSpinBox1.parentWidget().layout().replaceWidget(
            self.ui.testSpinBox1,
            self.scientificSpinBox
        )
        self.ui.testSpinBox1 = self.scientificSpinBox
        self.connectSlots()

    def onValueChangeSlot(self):
        self.ui.valueChangedLabel.setText("value: " + str(self.scientificSpinBox.value))
        self.ui.baseValueLabel.setText("baseValue: " + str(self.scientificSpinBox.baseValue))
        self.ui.baseUnitLabel.setText("baseUnit: " + str(self.scientificSpinBox.baseUnit))
        self.ui.baseQuantityLabel.setText("baseQuantity: " + str(self.scientificSpinBox.baseQuantity))

    def onTextChangeSlot(self):
        self.ui.textChangedLabel.setText("text: " + str(self.scientificSpinBox.text()))