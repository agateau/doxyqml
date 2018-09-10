/**
 * An item with readonly properties
 */
class ReadOnlyProperty : public Item {
public:
/**
     * A readonly property
     */
/** @remark This property is read-only */
Q_PROPERTY(real gravity)
/**
     * A read-write property
     */
Q_PROPERTY(real speed)
};
