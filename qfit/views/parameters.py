from PySide6.QtCore import QObject, Signal, Slot, Qt

from qfit.widgets.grouped_sliders import (
    LabeledSlider,
    GroupedWidgetSet,
    SPACING_BETWEEN_GROUPS,
)
from qfit.utils.helpers import clearChildren


class SliderParamView(QObject):
    def __init__(
        self, 
        *args, 
        **kwargs
    ):

        self.prefitSlidersInserts()
        self.prefitMinMaxInserts()
    

    def prefitSlidersInserts(self):
        """
        View init: pre-fit sliders

        Insert a set of sliders for the prefit parameters according to the parameter set
        """
        # remove the existing widgets, if we somehow want to rebuild the sliders
        clearChildren(self.ui.prefitScrollAreaWidget)

        # create a QWidget for the scrollArea and set a layout for it
        prefitScrollLayout = self.ui.prefitScrollAreaWidget.layout()

        # set the alignment of the entire prefit scroll layout
        prefitScrollLayout.setAlignment(Qt.AlignTop)

        # generate the slider set
        self.sliderSet = GroupedWidgetSet(
            widget_class=LabeledSlider,
            init_kwargs={"label_value_position": "left_right"},
            columns=1,
            parent=self.ui.prefitScrollAreaWidget,
        )

        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.parentNameByObj[key]

            self.sliderSet.addGroupedWidgets(
                group_name,
                list(para_dict.keys()),
            )

        prefitScrollLayout.addWidget(self.sliderSet)

        # add a spacing between the sliders and the min max table
        prefitScrollLayout.addSpacing(SPACING_BETWEEN_GROUPS)

    def prefitMinMaxInserts(self):
        """
        View init: pre-fit min max table
        """
        # remove the existing widgets, if we somehow want to rebuild the sliders
        clearChildren(self.ui.prefitMinmaxScrollAreaWidget)

        # create a QWidget for the minmax scroll area and set a layout for it
        prefitMinmaxScrollLayout = self.ui.prefitMinmaxScrollAreaWidget.layout()

        # set the alignment of the entire prefit minmax scroll layout
        prefitMinmaxScrollLayout.setAlignment(Qt.AlignTop)

        self.minMaxTable = FoldableTable(
            MinMaxItems,
            paramNumPerRow=1,
            groupNames=list(self.sliderParameterSet.parentNameByObj.values()),
        )
        self.minMaxTable.setCheckable(False)
        self.minMaxTable.setChecked(False)

        # insert parameters
        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.parentNameByObj[key]

            for para_name in para_dict.keys():
                self.minMaxTable.insertParams(group_name, para_name)

        # add the minmax table to the scroll area
        foldable_widget = FoldableWidget("RANGES OF SLIDERS", self.minMaxTable)
        prefitMinmaxScrollLayout.addWidget(foldable_widget)

        # default to fold the table
        foldable_widget.toggle()
